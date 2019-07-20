# 简化 ： 假设其中一个轴为0


def getRange(pts, ax):
    mx = pts[0][ax]
    mi = pts[0][ax]
    for p in pts:
        if p[ax] < mi:
            mi = p[ax]
        if p[ax] > mx:
            mx = p[ax]
    return mx - mi


def pts2flatten(pts):
    ret = []
    rg = [getRange(pts, i) for i in range(3)]
    deli = rg.index(min(rg))
    print("deli:", deli)
    rsvi = [i for i in range(3) if i != deli]
    for p in pts:
        ret.append([p[rsvi[0]], p[rsvi[1]]])
    return ret

import math
import numpy as np
from PIL import Image
size = 100
def pts2image(pts):
    x_range = [min(pts[:, 0]), max(pts[:, 0])]
    y_range = [min(pts[:, 1]), max(pts[:, 1])]
    x_w = int((x_range[1]-x_range[0])*size)
    y_w = int((y_range[1]-y_range[0])*size)

    arr = np.zeros((y_w+1, x_w+1), dtype=np.uint)
    print(arr.shape)
    print(len(pts))
    for p in pts:
        x = int((p[0]-x_range[0])*size)
        y = int((p[1]-y_range[0])*size)
        print(x,y)
        arr[y][x] = 255
    print(arr.shape)
    img = Image.fromarray(arr, '1')
    img.save('tmp.png')

# import pytesseract
from PIL import Image
#


#
def getNumAns(pts):
    pts
    image = Image.open('tmp.jpg')
    code = pytesseract.image_to_string(image)
    return code


import numpy as np
