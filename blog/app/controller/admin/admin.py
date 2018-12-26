from flask import request, jsonify, Flask, render_template
from app.controller.admin import  admin
from app.controller.home import  home

@admin.route('/index')
def hello():
    return render_template('admin/menu.html')
@admin.route('/login11')
def login():
    return  render_template('admin/user/login.html')