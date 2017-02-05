from difflib import SequenceMatcher
import string

printable = string.ascii_letters + string.digits + ' '
idir = "imgs"
fmt = "%x"


def hex_escape(s):
    return ''.join(escape(c) for c in s)


def escape(c):
    if c == "\n":
        return c
    c = ord(c)
    return str(c) + " "


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_rows(rects):
    rects2 = [[x[0], x[1], x[2], x[3], round(x[1]/200.0)*200.0] for x in rects]
    rects2 = sorted(rects2, key=lambda k: k[4])
    # for i in rects2:
    #     print i
    rs = set([x[4] for x in rects2])
    rs = sorted(list(rs))
    rows = []
    for k in rs:
        row = []
        for l in rects2:
            if l[4] == k:
               row.append(l)
        rows.append(row)
    return rows