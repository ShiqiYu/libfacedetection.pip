from .yudet import detect as c_detect

def detect(img, conf_thresh=50):
    '''
    @param img: numpy.ndarray, shape=(H, W, 3), dtype=uint8, BGR
    @param conf_thresh: float, confidence threshold, default=50, range=[0, 100]
    
    @return: 
        confs: numpy.ndarray, shape=(N,), dtype=uint16, confidence 
        bboxes: numpy.ndarray, shape=(N, 4), dtype=uint16, bounding box (XYWH)
        landmarks: numpy.ndarray, shape=(N, 10), dtype=uint16, landmarks (XYXYXYXYXY)
    '''
    result = c_detect(img)
    confs = result[:, 0]
    mask = confs > conf_thresh
    result = result[mask]    
    confs, bboxes, landmarks = result[:, 0], result[:, 1:5], result[:, 5:-1]
    return confs, bboxes, landmarks

