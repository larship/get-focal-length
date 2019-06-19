#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Скрипт возвращает фокусное расстояние фотографии из данных EXIF

import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS


def list_images(dir):
    def filter_images(filename):
        return filename.endswith('.jpg') or filename.endswith('.JPG')

    def get_full_path(filename):
        return dir + '/' + filename

    files = os.listdir(dir)
    images = list(map(get_full_path, filter(filter_images, files)))

    for name in files:
        if os.path.isdir(dir + '/' + name):
            images += list_images(dir + '/' + name)

    return images


def get_exif(filename):
    ret_exif = {}
    image = Image.open(filename)
    exif_info = image._getexif()

    if exif_info:
        for tag, value in exif_info.items():
            decoded = TAGS.get(tag, tag)
            ret_exif[decoded] = value

    return ret_exif


if len(sys.argv) == 1:
    print('Не указан путь к каталогу с фотографиями')
    sys.exit()
else:
    photos_dir = '/' + str(sys.argv[1]).strip('/')

images = list_images(photos_dir)

# Сортировка по дате изменения
date_list = [[image_name, os.path.getmtime(image_name)] for image_name in images]
files = sorted(date_list, key=lambda image_name: image_name[1], reverse=True)
images = list(map(lambda image_name: image_name[0], files))

for image_name in images:
    data = get_exif(image_name)

    if data.get('FocalLength'):
        print(image_name + ': FocalLength: ' + str(data.get('FocalLength')[0]) + ' мм')
    else:
        print(image_name + ': не удалось получить FocalLength')