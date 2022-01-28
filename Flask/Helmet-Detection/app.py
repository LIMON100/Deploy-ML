# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 12:42:28 2022

@author: limon
"""


from flask import Flask, render_template, Response,  request, session, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename

from PIL import Image
import os
import sys
import cv2

from infer_ker import *


app = Flask(__name__)
UPLOAD_FOLDER = 'I:/JumpWatts/axel/for-helmet/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      print(filename)
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      print(filepath)
      f.save(filepath)
      setup_inference(filepath, filename)
      
      return render_template("uploaded.html", display_detection = filename, fname = filename)      

if __name__ == '__main__':
   app.run(port=4001, debug=True)
