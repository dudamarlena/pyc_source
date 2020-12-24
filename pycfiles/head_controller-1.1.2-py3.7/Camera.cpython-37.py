# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/head_controller/Camera.py
# Compiled at: 2019-10-27 03:16:54
# Size of source mod 2**32: 2147 bytes
import cv2, time
import head_controller.Features as Features
import pandas as pd, numpy as np, json
import head_controller.db as db
import head_controller.Model as Model
RESIZE_FACTOR = 0.02

def check_video_frame_data():
    video = cv2.VideoCapture(0)
    check, frame = video.read()
    print(check)
    print(frame)
    video.release()


def check_video_frame_data_predict():
    m = Model.Model()
    print('training...')
    m.build_svc()
    print('done')
    start_time = time.time()
    video = cv2.VideoCapture(0)
    while time.time() - start_time < 2:
        print('calibrating camera')
        check, frame = video.read()
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    while True:
        check, frame = video.read()
        print(check)
        print(frame)
        orig = frame
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            continue

        gray = cv2.resize(gray, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
        time_ = time.time() * 1000.0
        X = np.array([int(x) for x in gray.ravel()])
        cv2.imshow('Image', orig)
        print('PREDICTION:', m.clf.predict(X.reshape(1, -1)))
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('w'):
            continue
        time.sleep(1)
        cv2.destroyAllWindows

    video.release()


def get_features():
    f = Features.Collector()
    df = f.get_key()
    return df


def capture_review_submit_labels():
    df = get_features()
    print('Sample Length:', len(df))
    resp = input('Enter Y to save training data: ')
    if resp.lower() == 'y':
        db.send_df_to_table(df, 'training_data_small', operation='append')
    else:
        df.to_csv('Rejected.csv')
    X, y = db.get_training_data()
    score = db.cross_validation_score_from_data(X, y)
    print('Cross validated with a score of {}'.format(score))