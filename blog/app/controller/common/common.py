from flask import request, jsonify, Flask, render_template
from app.controller.common import common


@common.route('/error404')
def hello():
    return render_template('home/index.html')


@common.app_errorhandler(404)
def hello1(error):
    return render_template('home/index.html')
    response = dict(status=0, message="404 Not Found")
    return jsonify(response), 404
