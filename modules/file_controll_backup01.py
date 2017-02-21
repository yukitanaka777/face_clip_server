# -*- encoding:utf-8 -*-

import os
import random
import string
import numpy as np
import cv2
import facetracker
from werkzeug.utils import secure_filename
from PIL import Image

conns = facetracker.LoadCon('./static/model/face.con')
trigs = facetracker.LoadTri('./static/model/face.tri')
tracker = facetracker.FaceTracker('./static/model/face.tracker')
cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
allow_extends = set(['png','jpeg','jpg','gif'])
digit = 8

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in allow_extends

def image_save(img):

  if img and allowed_file(img.filename):

    ImgName = img.filename
    result = "ok"
    img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
    image_gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
    if len(facerect) is 0:
      result = "no human"

    else:
      #result = facerect
      #tracker.setWindowSizes((11, 9, 7))
      #if tracker.update(image_gray):
      #  tracked_img = tracker.draw(img,conns,trigs)
      #  obj3D = tracker.get3DShape()
      #  obj2D = tracker.get2DShape()
      #  pos = tracker.getPosition()
      #  orient = tracker.getOrientation()
      #  attr = tracker.iterations
        #result = "no human"
      #  result = orient
      #  cv2.imwrite('./static/image/guest/'+secure_filename(ImgName),tracked_img)
      for clip in facerect:
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(digit)])
        dst = img[clip[1]-(clip[1]/3):clip[1]+clip[3]+((clip[1]+clip[3])/3),clip[0]:clip[0]+clip[2]]
        cv2.imwrite('./static/image/guest/'+secure_filename(random_str+ImgName),dst)
        result = './static/image/guest/'+secure_filename(random_str+ImgName)
        gray = cv2.cvtColor(dst, cv2.cv.CV_BGR2GRAY)
        try:
          if tracker.update(gray):
            tracked_img = tracker.draw(dst,conns,trigs)
            cv2.imwrite('./static/image/guest/'+secure_filename(ImgName),tracked_img)
            result = './static/image/guest/'+secure_filename(random_str+ImgName)

        except:
          result = "no face"

      #else:
      #  result = "failed tracking"

  else:
    result = "no"

  return result
