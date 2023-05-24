from .yuface import detect as c_detect
import warnings


def detect(img, conf=0.5):
    '''
    @param img: numpy.ndarray, shape=(H, W, 3), dtype=uint8, BGR
    @param conf_thresh: float, confidence threshold, default=0.5, range=[0.0, 1.0]
    
    @return: 
        confs: numpy.ndarray, shape=(N,), dtype=uint16, confidence 
        bboxes: numpy.ndarray, shape=(N, 4), dtype=uint16, bounding box (XYWH)
        landmarks: numpy.ndarray, shape=(N, 10), dtype=uint16, landmarks (XYXYXYXYXY)
    '''
    conf_thresh = conf * 100
    h, w, c = img.shape
    if h > 960 or w > 960:
        warnings.warn(f'Image size ({w}, {h}) is too large, it may cause detection performance degradation.')
    result = c_detect(img)
    confs = result[:, 0]
    mask = confs > conf_thresh
    result = result[mask]    
    confs, bboxes, landmarks = result[:, 0], result[:, 1:5], result[:, 5:-1]
    return confs, bboxes, landmarks

