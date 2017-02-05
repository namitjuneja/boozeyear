#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFilter
import sys
import numpy as np
import pyocr
import pyocr.builders
from scipy import ndimage
import re

from utils import *
from data import *

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % lang)


def find_match(name, sku):
    closest = (0, None, None)
    for n, s in brands.iteritems():
        score = similar(name, n)
        if score > closest[0]:
            closest2 = (0, None)
            for x in s:
                score2 = similar(sku, x)
                if score2 > closest2[0]:
                    closest2 = (score2, x)
                    # print score, n, score2, x
            closest = (score, n, closest2[1])
    return closest


def calc_price(p):
    print p
    if "$" in p:
        p = p.split("$")[1]
    p = p.replace(' ', '')
    p1 = re.sub('[^0-9]', '', p)
    if len(p) < 3:
        return -1
    if len(p1) >= 4:
        p = p1[-4:]
    if p[0] == "5":
        p = p[1:]
    if p[-1] != "9":
        p = p[:-1] + "9"
    if p[-2] != "4" and p[-2] != "9":
        if p[-2] == "A":
            p = p[:-2] + "4" + p[-1]
        elif p[-2] == "S":
            p = p[:-2] + "9" + p[-1]
        else:
            print p
            p = p[:-2] + "9" + p[-1]  # tukke wali
    p = re.sub('[^0-9]', '', p)
    p = p[:-2] + "." + p[-2:]
    p = float(p)
    return p


def faster_bradley_threshold(image, threshold=75, window_r=5):
    percentage = threshold / 100.
    window_diam = 2 * window_r + 1
    # convert image to numpy array of greyscale values
    img = np.array(image.convert('L')).astype(np.float)  # float for mean precision
    # matrix of local means with scipy
    means = ndimage.uniform_filter(img, window_diam)
    # result: 0 for entry less than percentage*mean, 255 otherwise
    height, width = img.shape[:2]
    result = np.zeros((height, width), np.uint8)  # initially all 0
    result[img >= percentage * means] = 255  # numpy magic :)
    # convert back to PIL image
    return Image.fromarray(result)


def get_text(name, i):  # i is a contour rect
    img2 = Image.open(idir + "/" + name)
    img2 = img2.crop((i[0] + 50, i[1], i[0] + i[2], i[1] + i[3]))
    # img2.show()
    img2 = img2.convert('L')
    # for x in range(50,100,5):
    #     for y in [3,5,7,9,10]:
    # print "-----------------------------------------"
    # print x,y
    img3 = faster_bradley_threshold(img2, 80, 7)
    img3.filter(ImageFilter.SMOOTH_MORE)
    # img3.show()
    # break

    txt = tool.image_to_string(
        img3,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    ).encode('utf-8')
    # print txt
    # print txt.split("\n")
    txta = txt.split("\n")
    txta = [x for x in txta if x.strip()]
    return txta


def get_data(txta):
    if txta and len(txta) == 3:
        bname = txta[0]
        sku = txta[1]
        price = txta[2]
        _, bname, sku = find_match(bname, sku)
        print bname
        print sku
        price = calc_price(price)
        print price
        return [bname, sku, price]
    else:
        print "Ignored"
        return None
