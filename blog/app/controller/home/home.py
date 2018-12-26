from flask import request, jsonify, Flask, render_template
from app.controller.home import  home
@home.route('/about')
def about():
   return render_template('home/index.html')