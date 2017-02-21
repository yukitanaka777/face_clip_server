# -*- encoding:utf-8 -*-

import os
import random
import string
import numpy as np
import cv2
import dlib
import base64
import re
import json
import modules.setRotateImg as setIM
from werkzeug.utils import secure_filename

PREDICTOR_PATH = "./shape_predictor_68_face_landmarks.dat"
allow_extends = set(['png','jpeg','jpg','gif'])
digit = 8

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in allow_extends

def image_save(img):

  if img and allowed_file(img.filename):
    ImgName = img.filename
    img = setIM.img_reset(img.read())
    img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    r = 400.0 / img.shape[1]
    dim = (400, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    image_gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
    #image_gray = cv2.resize(image_gray,(700,600))
    #img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    #img = cv2.resize(img,(700,600))
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    dets, scores, idx = detector.run(image_gray, 0)
    if len(dets) is 0:
      result = ["None Face",False,"no face",None]
    else:

      try:

        for clip in dets:
          #mask_pos = np.matrix([[p.x, p.y] for p in predictor(img, dets[0]).parts()])
          #marks = setIM.landmarks_to_clm(mask_pos)
          random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(digit)])
          dst = img[clip.top()-80:clip.bottom()+80,clip.left()-50:clip.right()+50]
          cv2.imwrite('./static/image/guest/'+secure_filename(random_str+ImgName),dst)
          result = ['./static/image/guest/'+secure_filename(random_str+ImgName),True,random_str,0]

      except:
        result = ['error',False,'error',None]
        return result

  else:
    result = ["no match allow",False,"no img",None]

  return result



def other_image_save(json_data):

  if json_data and allowed_file(json_data["imgName"]):
    first_coma = json_data["img"].find(',')
    base64img = json_data["img"][first_coma:]
    imgFile = base64.decodestring(base64img)
    imgFile = setIM.img_reset(imgFile)
    img = cv2.cvtColor(np.array(imgFile),cv2.COLOR_RGB2BGR)
    ImgName = json_data["imgName"]
    r = 400.0 / img.shape[1]
    dim = (400, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    image_gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    dets, scores, idx = detector.run(image_gray, 0)
    if len(dets) is 0:
      result = {"img":None,"result":"Not Found Face","random_id":None,"name":json_data["text"]}
    else:

      try:

        for clip in dets:
          random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(digit)])
          dst = img[clip.top()-80:clip.bottom()+80,clip.left()-50:clip.right()+50]
          convert,buffered =  cv2.imencode('.jpg', dst)
          buffered = base64.b64encode(buffered)
          result = {"img":buffered,"result":True,"random_id":random_str,"name":json_data['text']}

      except:
        result = {"img":None,"result":"error","random_id":None,"name":json_data["text"]}
        return result

  else:
    result = {"img":None,"result":"not allow file","random_id":None,"name":json_data["text"]}

  return result



def for_test_login_img(json_data):

  if json_data and allowed_file(json_data["imgName"]):
    first_coma = json_data["img"].find(',')
    base64img = json_data["img"][first_coma:]
    imgFile = base64.decodestring(base64img)
    imgFile = setIM.img_reset(imgFile)
    img = cv2.cvtColor(np.array(imgFile),cv2.COLOR_RGB2BGR)
    r = 400.0 / img.shape[1]
    dim = (400, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    image_gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    dets, scores, idx = detector.run(image_gray, 0)
    if len(dets) is 0:
      result = {"img":None}
    else:

      try:

        for clip in dets:
          dst = img[clip.top()-80:clip.bottom()+80,clip.left()-50:clip.right()+50]
          convert,buffered =  cv2.imencode('.jpg', dst)
          buffered = base64.b64encode(buffered)
          result = {"img":buffered}

      except:
        result = {"img":None}
        return result

  else:
    result = {"img":None}

  return result
