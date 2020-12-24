# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/marccdimage.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 15185 bytes
"""

Authors:
........
* Henning O. Sorensen & Erik Knudsen:
  Center for Fundamental Research: Metal Structures in Four Dimensions;
  Risoe National Laboratory;
  Frederiksborgvej 399;
  DK-4000 Roskilde;
  email:erik.knudsen@risoe.dk
* Jon Wright:
  European Synchrotron Radiation Facility;
  Grenoble (France)

marccdimage can read MarCCD and MarMosaic images including header info.

JPW : Use a parser in case of typos (sorry?)

"""
from __future__ import with_statement, print_function, absolute_import
import logging, struct
from .tifimage import TifImage
logger = logging.getLogger(__name__)
CDEFINITION = '\ntypedef struct frame_header_type {\n         /* File/header format parameters (256 bytes) */\n         UINT32        header_type;  /* flag for header type\n                                           (can be  used as magic number) */\n         char header_name[16];           /* header name (MMX) */\n         UINT32        header_major_version;   /* header_major_version  (n.) */\n         UINT32        header_minor_version;   /* header_minor_version  (.n) */\n         UINT32        header_byte_order;/* BIG_ENDIAN (Motorola,MIPS);\n                                            LITTLE_ENDIAN (DEC, Intel) */\n         UINT32        data_byte_order;  /* BIG_ENDIAN (Motorola,MIPS);\n                                            LITTLE_ENDIAN (DEC, Intel) */\n         UINT32        header_size;      /* in bytes                     */\n         UINT32        frame_type;       /* flag for frame type */\n         UINT32        magic_number;     /* to be used as a flag -\n                                            usually  to indicate new file */\n         UINT32        compression_type; /* type of image compression    */\n         UINT32        compression1;     /* compression parameter 1 */\n         UINT32        compression2;     /* compression parameter 2 */\n         UINT32        compression3;     /* compression parameter 3 */\n         UINT32        compression4;     /* compression parameter 4 */\n         UINT32        compression5;     /* compression parameter 4 */\n         UINT32        compression6;     /* compression parameter 4 */\n         UINT32        nheaders;         /* total number of headers      */\n         UINT32        nfast;            /* number of pixels in one line */\n         UINT32        nslow;            /* number of lines in image     */\n         UINT32        depth;            /* number of bytes per pixel    */\n         UINT32        record_length;    /* number of pixels between\n                                            succesive rows */\n         UINT32        signif_bits;      /* true depth of data, in bits  */\n         UINT32        data_type;        /* (signed,unsigned,float...) */\n         UINT32        saturated_value;  /* value marks pixel as saturated */\n         UINT32        sequence;         /* TRUE or FALSE */\n         UINT32        nimages;          /* total number of images - size of\n                                            each is nfast*(nslow/nimages) */\n         UINT32        origin;           /* corner of origin             */\n         UINT32        orientation;      /* direction of fast axis       */\n         UINT32        view_direction;   /* direction to view frame      */\n         UINT32        overflow_location;/* FOLLOWING_HEADER,  FOLLOWING_DATA */\n         UINT32        over_8_bits;      /* # of pixels with counts  255 */\n         UINT32        over_16_bits;     /* # of pixels with count  65535 */\n         UINT32        multiplexed;      /* multiplex flag */\n         UINT32        nfastimages;      /* # of images in fast direction */\n         UINT32        nslowimages;      /* # of images in slow direction */\n         UINT32        background_applied;/* flags correction has been applied\n                                              hold magic number ? */\n         UINT32        bias_applied;     /* flags correction has been applied\n                                             hold magic number ? */\n         UINT32        flatfield_applied;/* flags correction has been applied -\n                                              hold magic number ? */\n         UINT32        distortion_applied;/*flags correction has been applied -\n                                              hold magic number ? */\n         UINT32        original_header_type;    /* Header/frame type from  file\n                                                    that frame is read from */\n         UINT32        file_saved;         /* Flag that file has been  saved,\n                                              should be zeroed if modified */\n         char reserve1[(64-40)*sizeof(INT32)-16];\n\n         /* Data statistics (128) */\n         UINT32        total_counts[2];  /* 64 bit integer range = 1.85E19*/\n         UINT32        special_counts1[2];\n         UINT32        special_counts2[2];\n         UINT32        min;\n         UINT32        max;\n         UINT32        mean;\n         UINT32        rms;\n         UINT32        p10;\n         UINT32        p90;\n         UINT32        stats_uptodate;\n         UINT32        pixel_noise[MAXIMAGES]; /*1000*base noise value (ADUs) */\n         char reserve2[(32-13-MAXIMAGES)*sizeof(INT32)];\n\n         /* More statistics (256) */\n         UINT16 percentile[128];\n\n\n         /* Goniostat parameters (128 bytes) */\n         INT32 xtal_to_detector;  /* 1000*distance in millimeters */\n         INT32 beam_x;            /* 1000*x beam position (pixels) */\n         INT32 beam_y;            /* 1000*y beam position (pixels) */\n         INT32 integration_time;  /* integration time in  milliseconds */\n         INT32 exposure_time;     /* exposure time in milliseconds */\n         INT32 readout_time;      /* readout time in milliseconds */\n         INT32 nreads;            /* number of readouts to get this  image */\n         INT32 start_twotheta;    /* 1000*two_theta angle */\n         INT32 start_omega;       /* 1000*omega angle */\n         INT32 start_chi;         /* 1000*chi angle */\n         INT32 start_kappa;       /* 1000*kappa angle */\n         INT32 start_phi;         /* 1000*phi angle */\n         INT32 start_delta;       /* 1000*delta angle */\n         INT32 start_gamma;       /* 1000*gamma angle */\n         INT32 start_xtal_to_detector; /* 1000*distance in mm (dist in um)*/\n         INT32 end_twotheta;           /* 1000*two_theta angle */\n         INT32 end_omega;              /* 1000*omega angle */\n         INT32 end_chi;                /* 1000*chi angle */\n         INT32 end_kappa;              /* 1000*kappa angle */\n         INT32 end_phi;                /* 1000*phi angle */\n         INT32 end_delta;              /* 1000*delta angle */\n         INT32 end_gamma;              /* 1000*gamma angle */\n         INT32 end_xtal_to_detector;   /* 1000*distance in mm (dist in um)*/\n         INT32 rotation_axis;          /* active rotation axis */\n         INT32 rotation_range;         /* 1000*rotation angle */\n         INT32 detector_rotx;          /* 1000*rotation of detector  around X */\n         INT32 detector_roty;          /* 1000*rotation of detector  around Y */\n         INT32 detector_rotz;          /* 1000*rotation of detector  around Z */\n         char reserve3[(32-28)*sizeof(INT32)];\n\n         /* Detector parameters (128 bytes) */\n         INT32 detector_type;            /* detector type */\n         INT32 pixelsize_x;              /* pixel size (nanometers) */\n         INT32 pixelsize_y;              /* pixel size (nanometers) */\n         INT32 mean_bias;                        /* 1000*mean bias value */\n         INT32 photons_per_100adu;       /* photons / 100 ADUs */\n         INT32 measured_bias[MAXIMAGES];/* 1000*mean bias value for each image*/\n         INT32 measured_temperature[MAXIMAGES];  /* Temperature of each\n                                                    detector in milliKelvins */\n         INT32 measured_pressure[MAXIMAGES]; /* Pressure of each  chamber\n                                               in microTorr */\n         /* Retired reserve4 when MAXIMAGES set to 9 from 16 and\n            two fields removed, and temp and pressure added\n          char reserve4[(32-(5+3*MAXIMAGES))*sizeof(INT32)]\n         */\n\n         /* X-ray source and optics parameters (128 bytes) */\n         /* X-ray source parameters (8*4 bytes) */\n         INT32 source_type;              /* (code) - target, synch. etc */\n         INT32 source_dx;                /* Optics param. - (size  microns) */\n         INT32 source_dy;                /* Optics param. - (size  microns) */\n         INT32 source_wavelength;        /* wavelength  (femtoMeters) */\n         INT32 source_power;             /* (Watts) */\n         INT32 source_voltage;           /* (Volts) */\n         INT32 source_current;           /* (microAmps) */\n         INT32 source_bias;              /* (Volts) */\n         INT32 source_polarization_x;    /* () */\n         INT32 source_polarization_y;    /* () */\n         char reserve_source[4*sizeof(INT32)];\n\n         /* X-ray optics_parameters (8*4 bytes) */\n         INT32 optics_type;              /* Optics type (code)*/\n         INT32 optics_dx;                /* Optics param. - (size  microns) */\n         INT32 optics_dy;                /* Optics param. - (size  microns) */\n         INT32 optics_wavelength;        /* Optics param. - (size  microns) */\n         INT32 optics_dispersion;        /* Optics param. - (*10E6) */\n         INT32 optics_crossfire_x;       /* Optics param. - (microRadians) */\n         INT32 optics_crossfire_y;       /* Optics param. - (microRadians) */\n         INT32 optics_angle;             /* Optics param. - (monoch.\n                                                    2theta - microradians) */\n         INT32 optics_polarization_x;    /* () */\n         INT32 optics_polarization_y;    /* () */\n         char reserve_optics[4*sizeof(INT32)];\n\n         char reserve5[((32-28)*sizeof(INT32))];\n\n         /* File parameters (1024 bytes) */\n         char filetitle[128];            /*  Title                  */\n         char filepath[128];             /* path name for data  file  */\n         char filename[64];              /* name of data  file  */\n         char acquire_timestamp[32];     /* date and time of  acquisition */\n         char header_timestamp[32];      /* date and time of header  update  */\n         char save_timestamp[32];        /* date and time file  saved */\n         char file_comments[512];        /* comments, use as desired   */\n         char reserve6[1024-(128+128+64+(3*32)+512)];\n\n         /* Dataset parameters (512 bytes) */\n         char dataset_comments[512];     /* comments, used as desired   */\n         /* pad out to  3072 bytes */\n         char pad[3072-(256+128+256+(3*128)+1024+512)];\n\n         } frame_header;\n'
C_TO_STRUCT = {'INT32': 'i', 
 'UINT32': 'I', 
 'char': 'c', 
 'UINT16': 'H'}
C_SIZES = {'INT32': 4, 
 'UINT32': 4, 
 'char': 1, 
 'UINT16': 2}
MAXIMAGES = 9

def make_format(c_def_string):
    """
    Reads the header definition in c and makes the format
    string to pass to struct.unpack
    """
    lines = c_def_string.split('\n')
    fmt = ''
    names = []
    expected = 0
    for line in lines:
        if line.find(';') == -1:
            pass
        else:
            decl = line.split(';')[0].lstrip().rstrip()
            try:
                typ, name = decl.split()
            except ValueError:
                logger.debug('skipping: %s', line)
                continue

            if name.find('[') > -1:
                try:
                    num = name.split('[')[1].split(']')[0]
                    num = num.replace('MAXIMAGES', str(MAXIMAGES))
                    num = num.replace('sizeof(INT32)', '4')
                    times = eval(num)
                except Exception as error:
                    logger.error('%s Please decode %s', error, decl)
                    raise error

            else:
                times = 1
            try:
                fmt += C_TO_STRUCT[typ] * times
                names += [name] * times
                expected += C_SIZES[typ] * times
            except KeyError:
                continue

    return (
     names, fmt)


HEADER_NAMES, HEADER_FORMAT = make_format(CDEFINITION)

def interpret_header(header, fmt, names):
    """
    given a format and header interpret it
    """
    values = struct.unpack(fmt, header)
    hdr = {}
    i = 0
    for name in names:
        if name in hdr:
            if isinstance(values[i], str):
                hdr[name] = hdr[name] + values[i]
            else:
                try:
                    hdr[name].append(values[i])
                except AttributeError:
                    hdr[name] = [
                     hdr[name], values[i]]

        else:
            hdr[name] = values[i]
        i = i + 1

    return hdr


class MarccdImage(TifImage):
    __doc__ = ' Read in data in mar ccd format, also\n        MarMosaic images, including header info '
    DESCRIPTION = 'File format from MarCCD and MarMosaic images'
    DEFAULT_EXTENSIONS = [
     'mccd']

    def _readheader(self, infile):
        """
        Parser based approach
        Gets all entries
        """
        infile.seek(1024)
        hstr = infile.read(3072)
        self.header = interpret_header(hstr, HEADER_FORMAT, HEADER_NAMES)

    def _read(self, fname):
        """
        inherited from tifimage
        ... a marccd image *is a* tif image
        just with a header
        """
        return TifImage.read(self, fname)


marccdimage = MarccdImage