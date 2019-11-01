import glob
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
import os
import pandas as pd
import re
import shutil
from PIL import Image


def pdToXml(name, coordinates, size, folder):
    xml = ['<annotation>']
    xml.append("    <folder>{}</folder>".format(folder))
    xml.append("    <filename>{}</filename>".format(name))
    xml.append("    <source>")
    xml.append("        <database>Unknown</database>")
    xml.append("    </source>")
    xml.append("    <size>")
    xml.append("        <width>{}</width>".format(size["width"]))
    xml.append("        <height>{}</height>".format(size["height"]))
    xml.append("        <depth>3</depth>".format())
    xml.append("    </size>")
    xml.append("    <segmented>0</segmented>")

    i = 0

    while i < len(coordinates):
        x = ""
        while coordinates[i] != ' ':
            x += coordinates[i]
            i += 1
        x = int(x)
        i += 1
        y = ""
        while coordinates[i] != ' ':
            y += coordinates[i]
            i += 1
        y = int(y)
        i += 1
        w = ""
        while coordinates[i] != ' ':
            w += coordinates[i]
            i += 1
        w = int(w)
        i += 1
        h = ""
        while coordinates[i] != ',':
            h += coordinates[i]
            i += 1
        h = int(h)
        i += 1
        xmin = x
        ymin = y
        xmax = x+w
        ymax = y+h

        xml.append("    <object>")
        xml.append("        <name>Face</name>")
        xml.append("        <pose>Unspecified</pose>")
        xml.append("        <truncated>0</truncated>")
        xml.append("        <difficult>0</difficult>")
        xml.append("        <bndbox>")
        xml.append("            <xmin>{}</xmin>".format(int(xmin)))
        xml.append("            <ymin>{}</ymin>".format(int(ymin)))
        xml.append("            <xmax>{}</xmax>".format(int(xmax)))
        xml.append("            <ymax>{}</ymax>".format(int(ymax)))
        xml.append("        </bndbox>")
        xml.append("    </object>")
    xml.append('</annotation>')
    return '\n'.join(xml)


def generateArray(file):
    with open(file, "r") as f:
        return f.read().splitlines()


def display(Diccionarios, n):
    name = Diccionarios[n]['name']
    img = mpimg.imread(os.path.join("dataset/"+name))
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    ann = Diccionarios[n]['annotations']
    i = 0
    while i < len(ann):
        x = ""
        while ann[i] != ' ':
            x += ann[i]
            i += 1
        x = int(x)
        i += 1
        y = ""
        while ann[i] != ' ':
            y += ann[i]
            i += 1
        y = int(y)
        i += 1
        w = ""
        while ann[i] != ' ':
            w += ann[i]
            i += 1
        w = int(w)
        i += 1
        h = ""
        while ann[i] != ',':
            h += ann[i]
            i += 1
        h = int(h)

        rect = patches.Rectangle(
            (x, y), w, h, linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(rect)
        i += 1

    (h, w, _) = img.shape
    plt.show()


def transformCoordinates(coordinates, wmax, hmax):
    major_axis = ""
    x = 0

    while coordinates[x] != ' ':
        major_axis += coordinates[x]
        x += 1
    major_axis = float(major_axis)
    x += 1

    minor_axis = ""
    while coordinates[x] != ' ':
        minor_axis += coordinates[x]
        x += 1
    minor_axis = float(minor_axis)
    x += 1

    theta = ""
    while coordinates[x] != ' ':
        theta += coordinates[x]
        x += 1
    theta = float(theta)
    x += 1

    center_x = ""
    while coordinates[x] != ' ':
        center_x += coordinates[x]
        x += 1
    center_x = float(center_x)
    x += 1

    center_y = ""
    while coordinates[x] != ' ':
        center_y += coordinates[x]
        x += 1
    center_y = float(center_y)

    a = ((math.cos(theta)**2)*(major_axis**2)) + \
        ((math.sin(theta)**2)*(minor_axis**2))
    b = ((math.sin(theta)**2)*(major_axis**2)) + \
        ((math.cos(theta)**2)*(minor_axis**2))
    w = 2*math.sqrt(a)
    h = 2*math.sqrt(b)
    center_x -= w/2
    center_y -= h/2
    if (center_x + w) > wmax:
        w = w - (center_x + w - wmax)
    elif center_x < 0:
        w = (center_x) + w
        center_x = 1

    if (center_y + h) > hmax:
        h = (h - (center_y+h-hmax))
    elif center_y < 0:
        h = h-center_y
        center_y = 1
    h = int(h)
    w = int(w)
    center_y = int(center_y)
    center_x = int(center_x)

    return str(center_x)+' '+str(center_y)+' '+str(w)+' '+str(h)


folder = pd.Series(glob.glob("dataset/*.jpg"))
folder
labels = pd.Series(glob.glob("labels/*-ellipselist.txt"))
labels
a = 0
arrDiccionarios = list()
while a < len(labels):
    string = labels[a]
    arr = generateArray(string)
    i = 0
    while i < len(arr):
        x = re.search("\d*_\d*_\d*_big_img_", arr[i])
        if x:
            try:
                name = arr[i]+".jpg"
                img = mpimg.imread(os.path.join("dataset", name))
                (h, w, _) = img.shape
                annotations = ""
                j = 0
                while j < int(arr[i+1]):
                    data = arr[2+i+j]
                    data = transformCoordinates(data, w, h)
                    annotations = annotations + data + ','
                    j += 1
                dimensions = {
                    'width': w,
                    'height': h
                }
                dicc = {
                    'name': name,
                    'annotations': annotations,
                    'size': dimensions
                }

                st = pdToXml(dicc['name'], dicc['annotations'],
                             dicc['size'], "dataset")
                nameXML = dicc['name'].replace(".jpg", ".xml")
                file = open(os.path.join("dataset_clean", nameXML), 'w')
                file.write(str(st))
                file.close()

                shutil.copy("dataset/"+name, "dataset_clean")
                arrDiccionarios.append(dicc)
            except:
                print("{} not found...".format(arr[i]))
        i = i + 1

    a = a + 1
dicts = pd.Series(arrDiccionarios)
n = 6
display(dicts, n)
