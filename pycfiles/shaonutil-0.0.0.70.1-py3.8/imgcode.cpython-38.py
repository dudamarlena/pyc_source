# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\imgcode.py
# Compiled at: 2020-05-02 01:26:44
# Size of source mod 2**32: 7618 bytes
"""BarCode"""
try:
    reduce
except NameError:
    from functools import reduce
else:
    from barcode.writer import ImageWriter
    from imutils.video import VideoStream
    from barcode import __BARCODE_MAP
    from imutils.video import FPS
    from pyzbar import pyzbar
    from PIL import Image
    import numpy as np, shaonutil, barcode, imutils, qrcode, time, sys, cv2, PIL, os

    def calculate_checksum(data):
        """Calculates the checksum for EAN13-Code / EAN8-Code return type: Integer"""

        def sum_(x, y):
            return int(x) + int(y)

        evensum = reduce(sum_, data[-2::-2])
        oddsum = reduce(sum_, data[-1::-2])
        return (10 - (evensum + oddsum * 3) % 10) % 10


    def verify_data(data):
        """Verify the EAN encoded data"""
        verification_digit = int(data[(-1)])
        check_digit = data[:-1]
        return verification_digit == calculate_checksum(check_digit)


    def actual_data(decodedObjects):
        """Returns data without checksum digit for EAN type"""
        if len(decodedObjects) > 0:
            obj = decodedObjects[0]
            data = obj.data.decode('ascii')
        else:
            return False
            if 'ean' in obj.type.lower():
                if verify_data(data):
                    return data[:-1]
                return False
            else:
                return data


    def encode(type_, file_, data, rt='FILE'):
        """Encode the data as barcode or qrcode"""
        __BARCODE_MAP['qrcode'] = ''
        if type_.lower() not in __BARCODE_MAP:
            raise ValueError('BarCode Type invalid')
        elif type_ == 'qrcode':
            qr = qrcode.QRCode(version=1,
              error_correction=(qrcode.constants.ERROR_CORRECT_L),
              box_size=10,
              border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            if rt == 'OBJ':
                return img
            img.save(file_)
            return file_
        else:
            bar_class = barcode.get_barcode_class(type_)
            bar_class.default_writer_options['text_distance'] = 0.5
            bar_class.default_writer_options['quiet_zone'] = 1.8
            bar_class.default_writer_options['module_height'] = int(13.636363636363635)
            writer = ImageWriter()
            bar = bar_class(data, writer)
            to_be_resized = bar.render()
            del bar
            width, height = to_be_resized.size
            width = int(width / 1.2)
            newSize = (width, height)
            resized = to_be_resized.resize(newSize, resample=(PIL.Image.NEAREST))
            if rt == 'OBJ':
                if os.path.exists(file_):
                    os.remove(file_)
                return resized
            resized.save(file_)
            return file_


    def decode(infile, log=False):
        """Decode barcode or qrcode"""
        if os.path.exists(infile):
            im = cv2.imread(infile)
        else:
            if type(infile) == np.ndarray:
                im = infile
            else:
                data = False
                decodedObjects = pyzbar.decode(im)
                for obj in decodedObjects:
                    if log:
                        print('Type : ', obj.type)

            if log:
                print('Data : ', obj.data, '\n')
            return decodedObjects


    def markBarcode(im, decodedObjects):
        """Mark and show the detected barcode"""
        for decodedObject in decodedObjects:
            points = decodedObject.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=(np.float32)))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points
            n = len(hull)
            for j in range(0, n):
                cv2.line(im, hull[j], hull[((j + 1) % n)], (255, 0, 0), 3)
            else:
                return im


    def make_barcode_matrix(type_, unique_ids, row_number, column_number, filename):
        """Make barcode matrix image"""
        print('Making ' + str(row_number) + 'x' + str(column_number) + ' BarCode Matrix ...')
        if not len(unique_ids) == row_number * column_number:
            raise ValueError('number of ids not equal to row x column size')
        TwoDArray = np.array(unique_ids).reshape(row_number, column_number)
        column_img = []
        for row_ids in TwoDArray:
            row_img = [encode(type_, '', (row_ids[i]), rt='OBJ') for i in range(column_number)]
            row_concatenated_img = shaonutil.image.merge_horizontally(row_img)
            column_img.append(row_concatenated_img)
        else:
            shaonutil.image.merge_vertically(column_img, filename)
            print('Exported ' + str(row_number) + 'x' + str(column_number) + ' BarCode Matrix as ' + filename)


    def read_live_barcode(detection_threshold=50):
        """Live read the barcode and returns data"""
        detection_time = 'no detection'
        print('[INFO] starting video stream...')
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        fps = FPS().start()
        counter_i = 0
        previous_data = None
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = gray
            decodedObjects = decode(im, log=True)
            frame = markBarcode(frame, decodedObjects)
            data = actual_data(decodedObjects)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 255
            if key == 27:
                break
            fps.update()
            if data:
                if previous_data == data:
                    if counter_i == 1:
                        start_time = time.time()
                    counter_i += 1
                else:
                    counter_i = 0
            previous_data = data
            if counter_i > detection_threshold:
                detection_time = time.time() - start_time
                break

        fps.stop()
        print('[INFO] elasped time: {:.2f}'.format(fps.elapsed()))
        print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))
        cv2.destroyAllWindows()
        vs.stop()
        message = data
        return (message, detection_time)