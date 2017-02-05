#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from utils import *


def detect_contours(image, output_set):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # get contours
    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # discard areas that are too large
        # if h>300 and w>300:
        # continue

        # discard areas that are too small
        if h < 70 or w < 200:
            continue
        if h > 170 or w > 450:
            continue
        if y < 715 or (835 < y < 1770) or (1895 < y < 2770):
            continue
        output_set.add((x, y, w, h))


def process_contours(contours_set, silent=False):
    sorted_set = sorted(list(contours_set))
    if not silent:
        print "Length pre processing: ", len(contours_set)
    # for i in srects:
    #     cv2.rectangle(image, (i[0], i[1]), (i[0]+i[2], i[1]+i[3]),
    #                   (randint(0, 255), randint(0, 255), randint(0, 255)), 10)
    #
    #     # cv2.rectangle(image,(i[0],i[1]),(i[0]+i[2],i[1]+i[3]),(255,0,255),10)
    #
    # cv2.imwrite('data/contoured1.jpg', image)

    min_width = 220
    diff_top_right = 100
    diff_bottom_left = 30

    for i in sorted_set:
        for j in sorted_set:
            if i != j and i in contours_set and j in contours_set:
                if abs(i[0] - j[0]) < diff_top_right and abs(i[1] - j[1]) < diff_top_right:
                    if i[2] > min_width and j[2] > min_width:
                        if i[2] < j[2]:
                            contours_set.remove(j)
                        else:
                            contours_set.remove(i)
                    elif i[2] > min_width:
                        contours_set.remove(j)
                    elif j[2] > min_width:
                        contours_set.remove(i)
                    else:
                        contours_set.remove(i)
                        contours_set.remove(j)

                elif abs(i[0] + i[2] - j[2] - j[0]) < diff_bottom_left and abs(
                                                i[1] + i[3] - j[3] - j[1]) < diff_bottom_left:
                    if i[2] > min_width and j[2] > min_width:
                        if i[2] < j[2]:
                            contours_set.remove(j)
                        else:
                            contours_set.remove(i)
                    elif i[2] > min_width:
                        contours_set.remove(j)
                    elif j[2] > min_width:
                        contours_set.remove(i)
                    else:
                        contours_set.remove(i)
                        contours_set.remove(j)

    if not silent:
        print "Length post processing: ", len(contours_set)


def get_contours(name):
    rects = set()
    image = cv2.imread(idir + "/" + name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # greyscale
    # cv2.imshow("grey", gray)
    # cv2.waitKey(0)
    for thres in range(150, 251, 10):
        thresh, im_bw = cv2.threshold(gray, thres, 255, 0)  # threshold
        detect_contours(im_bw, rects)

        # (thresh, im_bw) = cv2.threshold(gray, 123, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # cv2.imshow("grey", im_bw)
        # cv2.waitKey(0)
        kernel = np.ones((3, 3), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        transformed = cv2.erode(im_bw, kernel, iterations=1)  # transform (erode/dilate)
        detect_contours(transformed, rects)
        # cv2.imshow("grey", transformed)
        # cv2.waitKey(0)
        transformed = cv2.dilate(transformed, kernel, iterations=1)  # transform (erode/dilate)
        detect_contours(transformed, rects)
        # cv2.imshow("grey", transformed)
        # cv2.waitKey(0)

        # break

    process_contours(rects, True)
    # Create rectangles for final contours
    srects = sorted(list(rects))
    # for i in srects:
    #     cv2.rectangle(image, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]),
    #                   (randint(0, 255), randint(0, 255), randint(0, 255)), 10)
    # cv2.rectangle(image,(i[0],i[1]),(i[0]+i[2],i[1]+i[3]),(255,0,255),10)

    # cv2.imwrite('data/contoured.jpg', image)
    return srects
