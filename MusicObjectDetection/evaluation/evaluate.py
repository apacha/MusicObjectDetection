import argparse
import numpy as np
import os

#
# Explanation HERE: https://medium.com/@jonathan_hui/map-mean-average-precision-for-object-detection-45c121a31173
# https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html
#


def compute_ap(recall, precision):
    """ Compute the average precision, given the recall and precision curves.
    Code originally from https://github.com/rbgirshick/py-faster-rcnn.
    # Arguments
        recall:    The recall curve (list).
        precision: The precision curve (list).
    # Returns
        The average precision as computed in py-faster-rcnn.
    """
    # correct AP calculation
    # first append sentinel values at the end
    mrec = np.concatenate(([0.], recall, [1.]))
    mpre = np.concatenate(([0.], precision, [0.]))

    # compute the precision envelope
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    # to calculate area under PR curve, look for points
    # where X axis (recall) changes value
    i = np.where(mrec[1:] != mrec[:-1])[0]

    # and sum (\Delta recall) * prec
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def get_data(csv_filepath):
    boxes = []
        
    csv_file = open(csv_filepath,'r')
    annotation_list = csv_file.read().splitlines()
    csv_file.close()
    
    categories = set()
    image_hashes = set()
    
    for idx, annotation in enumerate(annotation_list):
        # Skip header row, if it was produced
        if annotation.startswith('path_to_image'):
            continue
        entry_elements = annotation.split(',')
        
        if len(entry_elements) == 7:
            image_hash, top, left, bottom, right, category, score = entry_elements
            score = float(score)
        else:    
            image_hash, top, left, bottom, right, category = entry_elements
            score = None
        
        image_hash = os.path.basename(image_hash)
        left = float(left)
        top = float(top)
        right = float(right)
        bottom = float(bottom)
        
        box = {
                'image': image_hash,
                'left': left,
                'top': top,
                'right': right,
                'bottom': bottom,
                'category': category,
                'score': score
            }

        boxes.append(box)
        categories.add(category)
        image_hashes.add(image_hash)

    return boxes, categories, image_hashes


def compute_overlap(boxes, query_boxes):
    N = boxes.shape[0]
    K = query_boxes.shape[0]
    overlaps = np.zeros((N,K), dtype=np.float64)
    
    for k in range(K):
        box_area = ((query_boxes[k][2] - query_boxes[k][0] + 1) * (query_boxes[k][3] - query_boxes[k][1] + 1))
        
        for n in range(N):
            iw = (
                min(boxes[n, 2], query_boxes[k, 2]) -
                max(boxes[n, 0], query_boxes[k, 0]) + 1
            )
            
            if iw > 0:
                ih = (
                    min(boxes[n, 3], query_boxes[k, 3]) -
                    max(boxes[n, 1], query_boxes[k, 1]) + 1
                )
                
                if ih > 0:
                    ua = np.float64(
                        (boxes[n, 2] - boxes[n, 0] + 1) *
                        (boxes[n, 3] - boxes[n, 1] + 1) +
                        box_area - (iw * ih)
                    )
                    
                    overlaps[n, k] = iw * ih / ua
                    
    return overlaps


def get_ap(images, categories, pred_boxes, ann_boxes, iou_threshold):
    average_precisions = {}

    for category in categories:
        false_positives = np.zeros((0,))
        true_positives = np.zeros((0,))
        scores = np.zeros((0,))
        num_annotations = 0
        
        for image in images:
            
            category_image_annotations = [box for box in ann_boxes if box['image'] == image and box['category'] == category]
            category_image_annotation_boxes = np.array([[b['left'], b['top'], b['right'], b['bottom']] for b in category_image_annotations])
            num_annotations += len(category_image_annotations)
            
            # Sort according to score
            category_image_predictions = [box for box in pred_boxes if box['image'] == image and box['category'] == category]            
            # print(category_image_predictions)
            category_image_predictions = sorted(category_image_predictions, key=lambda k: -k['score'])
            
            #                 
            detected_annotations = []
            
            for prediction in category_image_predictions:
                scores = np.append(scores, prediction['score'])
                
                if len(category_image_annotations) == 0:
                    false_positives = np.append(false_positives,1)
                    true_positives = np.append(true_positives, 0)
                    continue
                
                overlaps = compute_overlap(np.expand_dims(np.array([prediction['left'], prediction['top'], prediction['right'], prediction['bottom']]),axis=0),
                                            category_image_annotation_boxes)
                
                assigned_annotation = np.argmax(overlaps, axis=1)
                max_overlap = overlaps[0, assigned_annotation]
                
                if max_overlap >= iou_threshold and assigned_annotation not in detected_annotations:
                    false_positives = np.append(false_positives, 0)
                    true_positives = np.append(true_positives, 1)
                    detected_annotations.append(assigned_annotation)
                else:
                    false_positives = np.append(false_positives,1)
                    true_positives = np.append(true_positives, 0)
                
        if num_annotations == 0:
            average_precisions[category] = [0, 0]
            continue
        
        # sort by score    
        indices = np.argsort(-scores)
        false_positives = false_positives[indices]
        true_positives = true_positives[indices]
        
        # compute false positives and true positives
        false_positives = np.cumsum(false_positives)
        true_positives = np.cumsum(true_positives)
        
        # compue recall and precision
        recall = true_positives / num_annotations
        precision = true_positives / np.maximum(true_positives + false_positives, np.finfo(np.float64).eps)
        
        # compute average precision
        average_precision = compute_ap(recall, precision)
        average_precisions[category] = [average_precision, num_annotations]

    return average_precisions


def get_metrics(average_precisions):
    meanAP = 0
    count = 0
    weightedmAP = 0
    weightedCount = 0
    
    for category in average_precisions:
        meanAP += average_precisions[category][0]
        count += 1
        weightedmAP += average_precisions[category][0] * average_precisions[category][1]
        weightedCount += average_precisions[category][1]
        
    meanAP /= count
    weightedmAP /= weightedCount
    
    return meanAP, weightedmAP
    

############################################################

parser = argparse.ArgumentParser(description='Evaluate music object detection from CSV files.')
parser.add_argument('-annotation',  dest='annotation', type=str, required=True,
                    help='Path to the annotation CSV file.')
parser.add_argument('-prediction',  dest='prediction', type=str, required=True,
                    help='Path to the prediction CSV file.')
parser.add_argument('-classes', dest='classes', action='store_true',
                    help='Whether to compute class-wise results as well.')
args = parser.parse_args()


ann_boxes, ann_categories , ann_images = get_data(args.annotation)
pred_boxes, pred_categories, pred_images = get_data(args.prediction)

images = ann_images | pred_images
categories = ann_categories | pred_categories

thresholds = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

ap_by_th = {}

for th in thresholds:  
    ap_by_th[th] = get_ap(images, categories, pred_boxes, ann_boxes, iou_threshold = th)
    

############
# Pascal: Only 0.5 IOU

mAP, weightedmAP = get_metrics(ap_by_th[0.5])
print('Pascal, IoU = 0.5')
print('\t', 'mAP', mAP, '\t', 'w-mAP', weightedmAP)

if args.classes:
    print()
    for cls in sorted(ap_by_th[0.5].keys()):
        print('\t\t', str(cls), '\t', ap_by_th[0.5][cls][0])


#############
# COCO: Average over different AP according to 10 different IOUs
print()
print()

global_ap = {}


for category in ap_by_th[th]:
    global_ap[category] = [0, 0]
    
    for th in ap_by_th:
        ap, count = ap_by_th[th][category]
        global_ap[category][0] += ap
        global_ap[category][1] += count
        
    global_ap[category][0] /= len(ap_by_th)
    global_ap[category][1] /= len(ap_by_th)


mAP, weightedmAP = get_metrics(global_ap)
print('COCO, IoU = [0.5:0.95:0.05]')
print('\t', 'mAP', mAP, '\t', 'w-mAP', weightedmAP)

if args.classes:
        print()
        for cls in sorted(global_ap.keys()):
            print('\t\t', str(cls), '\t', global_ap[cls][0])
