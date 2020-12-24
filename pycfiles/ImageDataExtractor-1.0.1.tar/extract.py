# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: imagedataextractor/extract.py
# Compiled at: 2019-05-16 11:15:11
import glob, datetime
from .scalebar_identification import *
from .particle_identification import *
from .rdf_functions import *
from .image_identification import TEMImageExtractor
from .figure_splitting import split_by_photo, split_by_grid

def main_detection(imgname, outputpath=''):
    """Where the detection happens.

    :param sting imgname: name of image file.
    :param string outputpath: path to output directory.

    :return list filteredvertices: list of vertices of particles in image.
    :return float scale: Scale of pixels in image (m/pixel).
    :return float conversion: unit of scalevalue 10e-6 for um, 10e-9 for nm.

    """
    img = cv2.imread(imgname)
    if img.shape[0] * img.shape[1] < 50000:
        print 'img smaller than 50k'
        return (None, None)
    else:
        scale, inlaycoords, conversion = scalebar_identification(img, outputpath, testing=imgname)
        filteredvertices, particlediscreteness = particle_identification(img, inlaycoords, testing=False)
        inverted = False
        if inverted is False:
            rows = len(img)
            cols = len(img[0])
            if len(img.shape) == 2:
                gimg = img
            else:
                gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if len(filteredvertices) > 0:
                arealist = particle_metrics_from_vertices(img, gimg, rows, cols, filteredvertices)[1]
                detection_ratio = sum(arealist) / float(rows * cols)
                mean_particlediscreteness = sum(particlediscreteness) / float(len(particlediscreteness))
            else:
                detection_ratio = 0
                mean_particlediscreteness = 0
                arealist = []
            if len(filteredvertices) < 3 or detection_ratio < 0.1 or mean_particlediscreteness < 30:
                filteredvertices_inverted, particlediscreteness_inv = particle_identification(img, inlaycoords, testing=True, invert=True)
                if len(filteredvertices_inverted) > 0:
                    if len(img.shape) == 2:
                        gimg = img
                    else:
                        gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    rows = len(img)
                    cols = len(img[0])
                    arealist_inv = particle_metrics_from_vertices(img, gimg, rows, cols, filteredvertices_inverted)[1]
                    mean_particlediscreteness_inv = -1 * sum(particlediscreteness_inv) / float(len(particlediscreteness_inv))
                    print (
                     sum(arealist_inv), sum(arealist))
                    print (mean_particlediscreteness_inv, mean_particlediscreteness)
                    if sum(arealist_inv) > sum(arealist) and mean_particlediscreteness_inv > mean_particlediscreteness:
                        filteredvertices = filteredvertices_inverted
                        inverted = True
        writeout_image(img, outputpath, filteredvertices, imgname, inverted)
        return (
         filteredvertices, scale, inverted, conversion)


def after_detection(imgname, filteredvertices, scale, inverted, conversion, outputpath=''):
    """After detection has happened calculate particle metrics and RDF.

    :param sting imgname: name of image file.
    :param list filteredvertices: list of vertices of particles (as numpy.ndarray) in image.
    :param float scale: Scale of pixels in image (m/pixel).
    :param float conversion: unit of scalevalue 10e-6 for um, 10e-9 for nm.
    :param string outputpath: path to output directory.

    :return float avgarea: average size of particles (m2)
    :return float avgcolormean: average pixel intensity in particles.
    :return list rdf: [x,y] columns of particle RDF.

    """
    img = cv2.imread(imgname)
    rows = len(img)
    cols = len(img[0])
    if len(img.shape) == 2:
        gimg = img
    else:
        gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resemblances, conclusion = match_to_shapes(filteredvertices, image_with_shapes=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shapes_to_match.png'))
    colorlist, arealist, avgcolormean, avgcolorstdev, avgarea = particle_metrics_from_vertices(img, gimg, rows, cols, filteredvertices)
    filtered_areas = remove_outliers(arealist)
    if len(filtered_areas) > 1:
        avgarea = np.median(filtered_areas) * scale ** 2
    else:
        avgarea = float(filtered_areas[0]) * scale ** 2
    om = int(math.floor(math.log10(avgarea)))
    avgarea = round(avgarea * 10 ** (-1 * om), 2) * 10 ** om
    arealist = [ a * scale ** 2 for a in arealist ]
    filtered_areas = [ a * scale ** 2 for a in filtered_areas ]
    particle_size_histogram(arealist, filtered_areas, imgname, outputpath)
    aspect_ratios_list = aspect_ratios(filteredvertices)
    mean_aspect_ratio = round(sum(aspect_ratios_list) / float(len(aspect_ratios_list)), 2)
    number_of_particles = len(filteredvertices)
    outfile = open(os.path.join(outputpath, imgname.split('/')[(-1)].split('.')[0] + '.txt'), 'w')
    outfile.write(imgname.split('/')[(-1)] + ' processed using ImageDataExtractor on ' + '\n')
    outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
    outfile.write('Article DOI: \n')
    outfile.write(imgname.split('/')[(-1)].split('_')[1] + '\n')
    outfile.write('Figure number: \n')
    outfile.write(imgname.split('/')[(-1)].split('_')[2] + '\n' + '\n')
    outfile.write(str(number_of_particles) + ' particles detected.' + '\n')
    outfile.write('Representative particle size: ' + str(avgarea) + ' sqm' + '\n' + '\n')
    outfile.write('Particle resemblances to regular shapes: ' + '\n')
    outfile.write(str(resemblances) + '\n')
    outfile.write(conclusion + '\n')
    outfile.write('Average aspect ratio: ' + str(mean_aspect_ratio) + '\n')
    if inverted == True:
        outfile.write('Image colors were inverted for a more accurate detection.' + '\n')
    outfile.close()
    xRDF = []
    yRDF = []
    if len(filteredvertices) > 9:
        xRDF, yRDF = calculate_rdf(filteredvertices, rows, cols, scale, increment=4, progress=True)
        output_rdf(xRDF, yRDF, imgname, conversion, outputpath)


def extract_images(path_to_images, outputpath='', path_to_secondary=None, path_to_already_done=None):
    """Runs scalebar and particle identification on an image document.

    :param string path_to_images: path to images of interest.
    :param string outputpath: path to output directory.
    :param string path_to_secondary: path to secondary directory, useful
    to skip certain images (if starting or restarting a batch) or process only
    a preapproved set. 

    """
    if os.path.isdir(path_to_images):
        images = [ os.path.join(path_to_images, img) for img in os.listdir(path_to_images) ]
    else:
        if os.path.isfile(path_to_images):
            images = [
             path_to_images]
        else:
            raise Exception('Unsupported input format')
        secondary = []
        if path_to_secondary != None:
            secondary.extend([ a.split('/')[(-1)][4:] for a in glob.glob(path_to_secondary) ])
        else:
            secondary = [ a.split('/')[(-1)] for a in images ]
        already_done = []
        if path_to_already_done != None:
            already_done.extend([ a.split('/')[(-1)][4:] for a in glob.glob(path_to_already_done) ])
        for imgname in images:
            if imgname.split('/')[(-1)] in secondary and imgname.split('/')[(-1)] not in already_done:
                print 'Scale and particle detection begun on: ' + str(imgname)
                imgoutputdir = os.path.join(outputpath, imgname.split('/')[(-1)].split('.')[0])
                if not os.path.exists(imgoutputdir):
                    os.makedirs(imgoutputdir)
                filteredvertices, scale, inverted, conversion = main_detection(imgname, imgoutputdir)
                if len(filteredvertices) > 0:
                    after_detection(imgname, filteredvertices, scale, inverted, conversion, imgoutputdir)
                else:
                    outfile = open(imgname.split('/')[(-1)].split('.')[0] + '.txt', 'w')
                    outfile.write(imgname.split('/')[(-1)] + '\n')
                    outfile.write('No particles found.')
                    outfile.close()

    return


extract_image = extract_images

def extract_documents(path_to_documents, path_to_images, outputpath='', path_to_secondary=None, path_to_already_done=None):
    """ Automatically detects SEM and TEM images from HTML/XML documents for extraction

    :param string path_to_documents : path to documents of interest
    :param string outputpath: path to output directory.
    :param string path_to_secondary: path to secondary directory, useful
    to skip certain images (if starting or restarting a batch) or process only
    a preapproved set.
    """
    extractor = TEMImageExtractor(path_to_documents, path_to_images, typ='tem')
    extractor.get_all_tem_imgs(parallel=False)
    split_figures(path_to_images)
    path_to_split_images = os.path.join(path_to_images, 'split_grid_images')
    extract_images(path_to_split_images, outputpath)


def extract_document(path_to_document, path_to_images='', outputpath=''):
    """ Automatically detects SEM and TEM images for a simple HTML/XML document"""
    extractor = TEMImageExtractor(path_to_document, path_to_images, typ='tem')
    extractor.get_tem_imgs()
    split_figures(path_to_images)
    path_to_split_images = os.path.join(path_to_images, 'split_grid_images')
    extract_images(path_to_split_images, outputpath)


def split_figures(input_dir, output_dir=''):
    """ Automatically splits hybrid images through photo detection and grid splitting"""
    input_dir_name = os.path.basename(input_dir)
    raw_imgs_path = os.path.join(input_dir, 'raw_images')
    raw_csv_path = os.path.join(input_dir, input_dir_name + '_raw.csv')
    split_photo_imgs_path = os.path.join(input_dir, 'split_photo_images')
    split_photo_csv_path = os.path.join(input_dir, input_dir_name + '_photo.csv')
    split_grid_imgs_path = os.path.join(input_dir, 'split_grid_images')
    split_by_photo(raw_imgs_path, raw_csv_path, split_photo_imgs_path, split_photo_csv_path, True)
    split_by_grid(split_photo_imgs_path, split_grid_imgs_path)