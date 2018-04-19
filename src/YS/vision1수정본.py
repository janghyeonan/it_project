# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:33:03 2018

@author: yunsang
"""

import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =' api 키입력'
#구글클라우드 불러오기 
from google.cloud import vision
from google.cloud.vision import types

# 클라이언트를 인스턴스.
client = vision.ImageAnnotatorClient()
# 파일네임 정의 
file_name =('windstruck.jpg')

# 로컬에서 이미지 불러들이기
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# 주석을 추가 할 이미지 파일의 이름
def detect_text(file):
    client = vision.ImageAnnotatorClient()

    with io.open(file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:') #텍스트를 인식하는 절 
    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:') # rgb 속성을 인식하는절(색상) 
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
     
    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tred: {}'.format(color.color.red))
        print('\tgreen: {}'.format(color.color.green))
        print('\tblue: {}'.format(color.color.blue))   

    response = client.web_detection(image=image)
    annotations = response.web_detection
# 웹상에서 누구와 얼마나 일치하는지 찾아낸다. 신기하지?
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

detect_text(file_name)
