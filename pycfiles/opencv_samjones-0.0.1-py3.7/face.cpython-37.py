# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\face.py
# Compiled at: 2019-07-25 03:09:37
# Size of source mod 2**32: 2499 bytes


def faces():
    import numpy as np, cv2, pickle
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('./recognizers/mtx.yml')
    labels = {'person_name': 1}
    with open('pickles/face-labels.pickle', 'rb') as (f):
        og_labels = pickle.load(f)
        labels = {v:k for k, v in og_labels.items()}
    cap = cv2.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for x, y, w, h in faces:
            print(x, y, w, h)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            img_item = '7.png'
            cv2.imwrite(img_item, roi_color)
            img_item = 'my-image.png'
            cv2.imwrite(img_item, roi_gray)
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            sub_face = frame[y:y + h, x:x + w]
            sub_face = cv2.GaussianBlur(sub_face, (23, 23), 30)
            frame[y:y + sub_face.shape[0], x:x + sub_face.shape[1]] = sub_face
            face_file_name = 'samjones.jpg'
            cv2.imwrite(face_file_name, frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 255 == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()