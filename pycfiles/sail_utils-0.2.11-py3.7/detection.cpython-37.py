# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\cv\object\detection.py
# Compiled at: 2020-04-07 01:46:40
# Size of source mod 2**32: 2530 bytes
"""
detection module for objects
"""
import cv2, grpc
from sail_utils import LOGGER
from sail_utils.cv.base import _Detector, _Mapper
from sail_utils.cv.object.config import DEFAULT_TIME_OUT, DST_SIZE, THRESHOLD
from sail_utils.cv.object.protobuf import inference_pb2, inference_pb2_grpc

def _unary_detect(stub, img, time_out=None):
    request = inference_pb2.ObjectDetectionRequest(request_info=__name__, model_version=0)
    img_encode = cv2.imencode('.jpg', img)[1]
    request.image_data = img_encode.tobytes()
    response_f = stub.DetectKeyObject.future(request)
    try:
        response = response_f.result(timeout=time_out)
    except grpc.FutureTimeoutError as exception:
        try:
            LOGGER.warning(f"grpc <{exception.__str__()}>. just skip")
            rtn_value = []
        finally:
            exception = None
            del exception

    else:
        rtn_value = response.objects
    return rtn_value


def _format(resp, epoch: int, threshold: float, calibrator: _Mapper):
    results = []
    for res in resp:
        if res.score >= threshold:
            box = res.box
            xmin = box.xmin
            ymin = box.ymin
            xmax = box.xmax
            ymax = box.ymax
            results.append(dict(location=(calibrator([int(xmin), int(ymin), int(xmax), int(ymax)])),
              time_stamp=epoch,
              score=(res.score),
              label=(res.label)))

    return sorted(results, key=(lambda x: x['time_stamp']))


class KeyObjectDetector(_Detector):
    __doc__ = '\n    class for key object detection\n    '

    def __init__(self, server, src_size, dst_size=DST_SIZE, threshold=THRESHOLD, timeout=DEFAULT_TIME_OUT):
        super().__init__(server, src_size, dst_size, threshold, timeout)

    def detect(self, img, epoch) -> list:
        """
        detect key object on one image
        :param img:
        :param epoch:
        :return:
        """
        img = self._mapper.resize(img)
        with grpc.insecure_channel(self._server) as (channel):
            stub = inference_pb2_grpc.KeyObjectDetectionStub(channel)
            resp = _unary_detect(stub, img, self._timeout)
            return _format(resp, epoch, self._threshold, self._mapper)