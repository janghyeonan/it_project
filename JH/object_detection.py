#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 02:55:03 2018

@author: janghyeonan
"""

import sys
sys.path
sys.path.append('/Users/janghyeonan/models/research') #path 경로 꼭 확인
sys.path.append('/Users/janghyeonan/models/research/object_detection/utils')

import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
from matplotlib import pyplot as plt
from PIL import Image
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
  
from object_detection.utils import label_map_util #utils이름을 object_detection.utils 로 해결
from object_detection.utils import visualization_utils as vis_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = '/Users/janghyeonan/models/research/object_detection/data/mscoco_label_map.pbtxt' #이걸로 해결
NUM_CLASSES = 90

opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())  

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)
PATH_TO_TEST_IMAGES_DIR = 'test_images'

TEST_IMAGE_PATHS = ['/Users/janghyeonan/models/research/object_detection/test_images/image1.jpg', '/Users/janghyeonan/models/research/object_detection/test_images/image2.jpg', '/Users/janghyeonan/PythonStudy/war.jpg'] ##이렇게 변경

IMAGE_SIZE = (12, 8)

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:        
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])        
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)        
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})
     
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict

for image_path in TEST_IMAGE_PATHS:
  image = Image.open(image_path)
  image_np = load_image_into_numpy_array(image)  
  image_np_expanded = np.expand_dims(image_np, axis=0)  
  output_dict = run_inference_for_single_image(image_np, detection_graph)  
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)
  plt.figure(figsize=IMAGE_SIZE)
  plt.imshow(image_np)


image = Image.open('/Users/janghyeonan/PythonStudy/poster/99701.jpg')    


def ttt(urll): 
    image = Image.open(urll)    
    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:        
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')        
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')        
        image_np = load_image_into_numpy_array(image)        
        image_np_expanded = np.expand_dims(image_np, axis=0)        
        (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})        
        
        vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)
        plt.figure(figsize=IMAGE_SIZE)
        plt.imshow(image_np)
        threshold = 0.5
        objects = []
        for index, value in enumerate(classes[0]):          
          if scores[0, index] > threshold:
            objects.append((category_index.get(value)).get('name'))        
        Ndict = {}
        for i in objects:
            if i in Ndict.keys() :
                Ndict[i] += 1
            else:
                Ndict[i] = 1
        return Ndict


#이걸로 실행해
a = ttt('/Users/janghyeonan/PythonStudy/poster/157962.jpg')
a
b = ttt('/Users/janghyeonan/PythonStudy/movie_image.jpg')
b
c = ttt('/Users/janghyeonan/PythonStudy/r_movie_image.jpg')
c

from PIL import Image
img = Image.open('/Users/janghyeonan/PythonStudy/movie_image.jpg')
img = Image.open('/Users/janghyeonan/PythonStudy/poster/132423.jpg')
(img_h, img_w) = img.size
print(img.size)

img2 = Image.open('/Users/janghyeonan/PythonStudy/poster/145639.jpg')
(img_h, img_w) = img2.size
print(img2.size)


img2 = img.resize((3000, 4000)) #사이즈를 정하고
img2.save('/Users/janghyeonan/PythonStudy/r_movie_image.jpg') #저장하기

#############
def image_crop( infilename , save_path):
    img = Image.open( infilename )
    (img_h, img_w) = img.size
    print(img.size)
 
    # crop 할 사이즈 : grid_w, grid_h
    grid_w = int((img_h)/1.5) # crop width
    grid_h = int((img_w)/2.5) # crop height
    range_w = (int)(img_w/grid_w)
    range_h = (int)(img_h/grid_h)
    print(range_w, range_h)


    i = 0
 
    for w in range(range_w):
        for h in range(range_h):
            bbox = (h*grid_h, w*grid_w, (h+1)*(grid_h), (w+1)*(grid_w))
            print(h*grid_h, w*grid_w, (h+1)*(grid_h), (w+1)*(grid_w))
            # 가로 세로 시작, 가로 세로 끝
            crop_img = img.crop(bbox)
 
            fname = "{}.jpg".format("{0:05d}".format(i))
            savename = save_path + fname
            crop_img.save(savename)
            print('save file ' + savename + '....')
            i += 1
#######
image_crop('/Users/janghyeonan/PythonStudy/r_movie_image.jpg', '/Users/janghyeonan/PythonStudy/')
#####
lit =[]
for i in range(1,3):
    lit.append(ttt('/Users/janghyeonan/PythonStudy/0000'+str(i)+'.jpg'))
lit    
    


