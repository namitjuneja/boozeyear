#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from dateutil.parser import parse

from box_detect import *
from ocr import *
from utils import *

data = {}
mismatches = {}


def mismatch_rows(rows, holder, date):
    c = 0
    for i in range(3):
        row = []
        for e in rows[i]:
            if not tuple(e[:4]) in holder:
                continue
            val = holder[tuple(e[:4])]
            row.append(tuple(val[:2]))
        test_row = order[i]
        for x in range(len(test_row)):
            for y in range(len(row)):
                if test_row[x] == row[y]:
                    for z in range(y+1,len(row)):
                        for k in range(0, x):
                            if test_row[k] == row[z] and (row[y] != row[z] and abs(y-z) == 1):
                                print row
                                print test_row
                                print test_row[k], row[z]
                                print x, y, z, k
                                c += 1
    mismatches[date] = c

for name in os.listdir(idir):
    if name.startswith("Super") and name.endswith(".jpg"):  # and "-01-25" in name:
        print "-----------------------------------------"
        print name
        date = name[12:-4]
        date = parse(date)
        date = date.strftime(fmt)
        data[date] = {}
        holder = {}
        # CALL TO box_detect#get_contours
        srects = get_contours(name)

        rows = get_rows(srects)

        for i in srects:
            print "-----------------------------------------"

            # CALL TO ocr#get_text
            txta = get_text(name, i)
            # print txta

            # CALL TO ocr#get_data
            out = get_data(txta)
            if out:
                bname, sku, price = out
                if bname not in data[date]:
                    data[date][bname] = {}
                data[date][bname][sku] = price

                holder[tuple(i)] = [bname, sku, price]

        mismatch_rows(rows, holder, date)

        for n, s in brands.iteritems():
            if n not in data[date]:
                data[date][n] = {}
            for x in s:
                if x not in data[date][n]:
                    data[date][n][x] = -1

        with open('data/result.json', 'w') as fp:
            json.dump(data, fp)

        with open('data/mmresult.json', 'w') as fp:
            json.dump(mismatches, fp)
        # break
