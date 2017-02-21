# -*- encoding:utf-8 -*-

from flask import Flask,request,redirect,render_template,url_for,jsonify
from flask_cors import CORS,cross_origin
import modules.file_controll as Fc
import json

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADER'] = 'Content-Type'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/getPicture',methods=['GET','POST'])
def getPicture():
  if request.method == 'POST':

    if 'faceImg' not in request.files:
      print "no files"
      return redirect('http://192.168.1.6:5000/takePicture?message="no files"')

    url,result,user_id,mask_pos = Fc.image_save(request.files['faceImg'])
    if result:
      #mask_pos = mask_pos.tolist()
      return render_template('getPicture.html',imgUrl={"url":url,"name":request.form['user_name'],"id":user_id,"mask_pos":mask_pos})
      #return redirect('http://192.168.1.6:5000/takePicture?message='+str(url)+'')

    else:
      print url
      return redirect('http://192.168.1.6:5000/takePicture?message='+str(url)+'')

  else:

    return render_template('index.html')

@app.route('/myFace')
def myFace():
  return render_template('myface.html')

@app.route('/testPost',methods=['GET','POST'])
@cross_origin('*')
def tetes():

  if request.method == 'POST':
    json_data = request.get_json()
    result = Fc.other_image_save(json_data)

  else:
    reuslt =  "no"

  try:
    return jsonify(result)

  except:
    print "failed"


@app.route('/for_login_img_Post',methods=['GET','POST'])
@cross_origin('*')
def for_login_attach():

  if request.method == 'POST':
    json_data = request.get_json()
    result = Fc.for_test_login_img(json_data)

  else:
    reuslt =  "no"

  try:
    return jsonify(result)

  except:
    print "failed"

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0',port=8000)
