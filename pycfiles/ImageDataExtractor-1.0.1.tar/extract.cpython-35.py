# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edward/github/ImageDataExtractor/imagedataextractor/extract.py
# Compiled at: 2019-08-22 12:06:51
# Size of source mod 2**32: 17336 bytes
import glob, datetime, zipfile, tarfile
from PIL import Image
from .scalebar_identification import *
from .particle_identification import *
from .rdf_functions import *
from .image_identification import TEMImageExtractor
from .figure_splitting import split_by_photo, split_by_grid
from .img_utils import convert_gif_to_png

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
        raise Exception('Image too small for accurate extraction')
    scale, inlaycoords, conversion = scalebar_identification(img, outputpath, testing=imgname)
    filteredvertices, particlediscreteness = particle_identification(img, inlaycoords, testing=False)
    inverted = False
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
    arealist = [a * scale ** 2 for a in arealist]
    filtered_areas = [a * scale ** 2 for a in filtered_areas]
    if len(arealist) > 1 and len(filtered_areas) > 1:
        particle_size_histogram(arealist, filtered_areas, imgname, outputpath, conversion)
    aspect_ratios_list = aspect_ratios(filteredvertices)
    mean_aspect_ratio = round(sum(aspect_ratios_list) / float(len(aspect_ratios_list)), 2)
    number_of_particles = len(filteredvertices)
    outfile = open(os.path.join(outputpath, imgname.split('/')[(-1)].split('.')[0] + '.txt'), 'w')
    filename = imgname.split('/')[(-1)]
    if len(filename.split('_')) == 2:
        outfile.write(filename + ' processed using ImageDataExtractor on ' + '\n')
        outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
        outfile.write('Article DOI: \n')
        outfile.write(filename.split('_')[1] + '\n')
        outfile.write('Figure number: \n')
        outfile.write(filename.split('_')[2] + '\n' + '\n')
    else:
        outfile.write(filename + ' processed using ImageDataExtractor on ' + '\n')
        outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
    outfile.write(str(number_of_particles) + ' particle(s) detected.' + '\n')
    if conversion == 1:
        outfile.write('Representative particle size: ' + str(avgarea) + ' sqpx' + '\n' + '\n')
    else:
        outfile.write('Representative particle size: ' + str(avgarea) + ' sqm' + '\n' + '\n')
    outfile.write('Particle resemblances to regular shapes: ' + '\n')
    for i in resemblances:
        outfile.write(str(i) + ' ')

    outfile.write('\n')
    outfile.write(conclusion + '\n')
    outfile.write('Average aspect ratio: ' + str(mean_aspect_ratio) + '\n')
    if conversion == 1:
        outfile.write('***All units are in pixels as scale of image could not be determined.' + '\n')
    if inverted == True:
        outfile.write('Image colors were inverted for a more accurate detection.' + '\n')
    outfile.close()
    xRDF = []
    yRDF = []
    if len(filteredvertices) > 9:
        xRDF, yRDF = calculate_rdf(filteredvertices, rows, cols, scale, increment=30, progress=True)
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
        images = [os.path.join(path_to_images, img) for img in os.listdir(path_to_images)]
    else:
        if os.path.isfile(path_to_images):
            if path_to_images.endswith('zip'):
                print('Opening zip file...')
                zip_ref = zipfile.ZipFile(path_to_images)
                extracted_path = os.path.join(os.path.dirname(path_to_images), 'extracted')
                if not os.path.exists(extracted_path):
                    os.makedirs(extracted_path)
                zip_ref.extractall(extracted_path)
                zip_ref.close()
                images = [os.path.join(extracted_path, img) for img in os.listdir(extracted_path)]
            else:
                if path_to_images.endswith('tar.gz'):
                    print('Opening tarball file...')
                    tar_ref = tarfile.open(path_to_images, 'r:gz')
                    extracted_path = os.path.join(os.path.dirname(path_to_images), 'extracted')
                    if not os.path.exists(extracted_path):
                        os.makedirs(extracted_path)
                    tar_ref.extractall(extracted_path)
                    tar_ref.close()
                    images = [os.path.join(extracted_path, img) for img in os.listdir(extracted_path)]
                else:
                    if path_to_images.endswith('tar'):
                        print('Opening tarball file...')
                        tar_ref = tarfile.open(path_to_images, 'r:')
                        extracted_path = os.path.join(os.path.dirname(path_to_images), 'extracted')
                        if not os.path.exists(extracted_path):
                            os.makedirs(extracted_path)
                        tar_ref.extractall(extracted_path)
                        tar_ref.close()
                        images = [os.path.join(extracted_path, img) for img in os.listdir(extracted_path)]
                    else:
                        images = [
                         path_to_images]
        else:
            raise Exception('Unsupported input format')
        secondary = []
        if path_to_secondary != None:
            secondary.extend([a.split('/')[(-1)][4:] for a in glob.glob(path_to_secondary)])
        else:
            secondary = [a.split('/')[(-1)] for a in images]
    already_done = []
    if path_to_already_done != None:
        already_done.extend([a.split('/')[(-1)][4:] for a in glob.glob(path_to_already_done)])
    for imgname in images:
        if imgname.split('.')[(-1)] == 'gif':
            imgname, secondary = convert_gif_to_png(imgname, secondary)
        if imgname.split('/')[(-1)] in secondary and imgname.split('/')[(-1)] not in already_done:
            print('Scale and particle detection begun on: ' + str(imgname))
            imgoutputdir = os.path.join(outputpath, imgname.split('/')[(-1)].split('.')[0])
            if not os.path.exists(imgoutputdir):
                os.makedirs(imgoutputdir)
            filteredvertices, scale, inverted, conversion = main_detection(imgname, imgoutputdir)
            if filteredvertices == None:
                outfile = open(os.path.join(imgoutputdir, imgname.split('/')[(-1)].split('.')[0] + '.txt'), 'w')
                filename = imgname.split('/')[(-1)]
                if len(filename.split('_')) == 2:
                    outfile.write(filename + ' processed using ImageDataExtractor on ' + '\n')
                    outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
                    outfile.write('Article DOI: \n')
                    outfile.write(filename.split('_')[1] + '\n')
                    outfile.write('Figure number: \n')
                    outfile.write(filename.split('_')[2] + '\n' + '\n')
                else:
                    outfile.write(filename + ' processed using ImageDataExtractor on ' + '\n')
                    outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
                outfile.write('Image does not meet resolution requirements.')
                outfile.close()
            else:
                if len(filteredvertices) > 0:
                    after_detection(imgname, filteredvertices, scale, inverted, conversion, imgoutputdir)
                else:
                    if len(filename.split('_')) == 2:
                        outfile.write(filename + ' processed using ImageDataExtractor on ' + '\n')
                        outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
                        outfile.write('Article DOI: \n')
                        outfile.write(filename.split('_')[1] + '\n')
                        outfile.write('Figure number: \n')
                        outfile.write(filename.split('_')[2] + '\n' + '\n')
                    else:
                        outfile.write(filename + ' processed using ImageDataExtractor on ' + '\n')
                        outfile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')


extract_image = extract_images

def extract_documents(path_to_documents, path_to_images='', outputpath='', path_to_secondary=None, path_to_already_done=None):
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