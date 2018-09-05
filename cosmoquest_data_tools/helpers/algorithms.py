import numpy as np


def non_maximum_suppression(bounding_boxes, overlap_threshold=0.1):
    if not len(bounding_boxes):
        return list()

    if isinstance(bounding_boxes, list):
        bounding_boxes = np.array(bounding_boxes)

    if not isinstance(bounding_boxes, np.ndarray):
        raise TypeError("Provided 'bounding_boxes' should be a numpy array...") 

    if bounding_boxes.dtype.kind == "i":
        bounding_boxes = bounding_boxes.astype("float")

    mask = list()

    y0 = bounding_boxes[:,0]
    x0 = bounding_boxes[:,1]
    y1 = bounding_boxes[:,2]
    x1 = bounding_boxes[:,3]

    area = (x1 - x0 + 1) * (y1 - y0 + 1)
    indices = np.argsort(y1)

    while len(indices) > 0:
        last = len(indices) - 1

        i = indices[last]
        mask.append(i)

        yy0 = np.maximum(y0[i], y0[indices[:last]])
        xx0 = np.maximum(x0[i], x0[indices[:last]])
        yy1 = np.minimum(y1[i], y1[indices[:last]])
        xx1 = np.minimum(x1[i], x1[indices[:last]])

        width = np.maximum(0, xx1 - xx0 + 1)
        height = np.maximum(0, yy1 - yy0 + 1)

        overlap = (width * height) / area[indices[:last]]

        indices = np.delete(indices, np.concatenate(([last], np.where(overlap > overlap_threshold)[0])))

    return bounding_boxes[mask].astype("int")
