import numpy as np
from PIL import Image
import os


def img_crop(im, w, h):
    list_patches = []
    imgwidth = im.shape[0]
    imgheight = im.shape[1]
    is_2d = len(im.shape) < 3
    for i in range(0, imgheight, h):
        for j in range(0, imgwidth, w):
            if is_2d:
                im_patch = im[j:j+w, i:i+h]
            else:
                im_patch = im[j:j+w, i:i+h, :]
            list_patches.append(im_patch)
    return list_patches


def value_to_class(v, foreground_thresh):
    df = np.sum(v)
    if df > foreground_thresh:
        # Road
        return 1
    else:
        # Background
        return 0


def get_precision_recall_accuracy(preds, labels):
    """
    Compute precision, recall and accuracy.
    :param preds: Predictions.
    :param labels: Labels or ground truths.
    :return: Precision, recall, accuracy.
    """
    preds = np.ravel(preds)
    labels = np.ravel(labels)
    # Compute true positives, false positives, false negatives and true negatives
    tp = len(np.where(np.logical_and(preds == 1, labels == 1))[0])
    fp = len(np.where(np.logical_and(preds == 1, labels == 0))[0])
    fn = len(np.where(np.logical_and(preds == 0, labels == 1))[0])
    tn = len(np.where(np.logical_and(preds == 0, labels == 0))[0])

    # Compute precision recall and accuracy
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    accuracy = (tp + tn) / (tp + fp + fn + tn)

    return precision, recall, accuracy


def get_f1(preds, labels):
    """
    Compute F1 score.
    :param preds: Predictions.
    :param labels: Labels or ground truths.
    :return: F1 score.
    """
    precision, recall, _ = get_precision_recall_accuracy(preds, labels)
    f1_score = (2 * precision * recall) / (precision + recall)
    return f1_score


def get_output_filenames(args):
    def _generate_name(fn):
        split = os.path.splitext(fn)
        return f'{split[0]}_OUT{split[1]}'

    return args.output or list(map(_generate_name, args.input))


def mask_to_image(mask):
    if mask.ndim == 2:
        return Image.fromarray((mask * 255).astype(np.uint8))
    elif mask.ndim == 3:
        return Image.fromarray((np.argmax(mask, axis=0) * 255 / mask.shape[0]).astype(np.uint8))


def plot_img_and_mask(image, mask):
    # TODO: Check this function
    pass
