from time import time

import time
from flask import request, jsonify, Flask, render_template, session, redirect, url_for, g

from app import db
from app.controller.admin import user
from app.controller.home import home
from app.models.Users import Users
from function import Common
from app.controller.auth import Auth
from app.models.Categories import Categories
from app.models.Permission import Permission


@user.route('/index')
def index():
    return '111'


@user.route('/register', methods=['POST'])
def register():
    if request.method != 'POST':
        Common.to_json('error', [])
    username = request.form.get('username')
    password = request.form.get('password')
    userExit = db.session.query(Users).filter(Users.name == username).first()
    if userExit is not None:
        return Common.to_json('error', dict(msg='用户名已经存在'))
    else:
        dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item = Users(name=username, password=password, address='1', tel='132111111', add_time=dateTime)
        db.session.add(item)
        res = db.session.commit()
        return Common.to_json('success', dict(msg='注册成功'))


@user.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return Common.to_json('error', [])
    username = request.json.get('username')
    password = request.json.get('password')
    userExit = db.session.query(Users).filter(Users.name == username).first()
    if userExit is None:
        return Common.to_json('error', dict(msg='用户不存在'))

    if userExit and userExit.check_login_password(password):
        login_time = int(time.time())
        token = Auth.generate_jwt(userExit.id, login_time)
        return Common.to_json('success', dict(
            userinfo=dict(username=userExit.name), token=token['jwt'], refresh_token=token['refresh_token']))
    else:
        return Common.to_json('error', dict(msg='密码错误'))


@user.route('/refreshCode', methods=['post'])
@Auth.require_jwt
def refresh_token():
    refresh_token = request.form.get('refresh_token')
    return jsonify(Auth.get_jwt_by_refresh_code(refresh_token))


@user.route('/getInfo', methods=['post'])
@Auth.require_jwt
def getInfo():
    return jsonify(Auth.decode_jwt(g.authorization))


@user.route('/authenticateUrl', methods=['post'])
@Auth.require_jwt
def authenticatePermission():
    url = request.json.get('url')
    if Auth.authenticatePermission(url):
        return Common.to_json('success')
    return Common.to_json('error')


@user.route('/getMenu', methods=['post'])
@Auth.require_jwt
def getMenuList():
    res = Auth.permission()
    return jsonify(res)


@user.route('/getRouter', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def getRouter():
    categoriesList = db.session.query(Categories).all()
    res = []
    for index, items in enumerate(categoriesList):
        item = dict(id=items.id, date=str(items.create_time), icon=items.icon, url=items.url, parent_id=items.parent_id,
                    name=items.name)
        res.append(item)
    res = Common.to_json('success', res)
    return res


@user.route('/addRouter', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def addRouter():
    name = request.json.get('name')
    url = request.json.get('url')
    parent_id = request.json.get('parent_id')
    icon = request.json.get('icon')
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    router = Categories(name=name, url=url, parent_id=parent_id, icon=icon, create_time=create_time)
    db.session.add(router)
    result = db.session.commit()
    return Common.to_json('success')


@user.route('/getRouterByid', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def getRouterByid():
    id = request.json.get('id')
    router = db.session.query(Categories).filter(Categories.id == id).first()
    res = dict(id=router.id, name=router.name, url=router.url, icon=router.icon, parent_id=router.parent_id)
    return Common.to_json('success', res)


@user.route('/delRouterByid', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def delRouterByid():
    id = request.json.get('id')
    # item = db.session.query()
    result = Categories.query.filter_by(id=id).delete()
    str(result)
    # if()
    return Common.to_json('success')
    # db.session.query(Categories.id == id)


@user.route('/updateRouter', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def updateRouter():
    id = request.json.get('id')
    name = request.json.get('name')
    url = request.json.get('url')
    parent_id = request.json.get('parent_id')
    icon = request.json.get('icon')
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item = db.session.query(Categories).filter_by(id=id).first()
    item.name = name
    item.url = url
    item.parent_id = parent_id
    item.icon = icon
    item.create_time = create_time
    db.session.add(item)
    result = db.session.commit()
    return Common.to_json('success')


@user.route('/getPermissionList', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def getPermissionList():
    res = db.session.query(Permission).all()

    response = []
    for i in res:
        item = dict(id=i.id, permission=i.permission, user_id=i.user_id, create_time=str(i.create_time),
                    creator=i.creator)
        response.append(item)
    return Common.to_json('success', response)


@user.route('/getPermissionByid', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def getPermissionByid():
    id = request.json.get('id')
    res = db.session.query(Permission).filter(Permission.id == id).first()
    item = dict(id=res.id, user_id=res.user_id, permission=res.permission, create_time=str(res.create_time))
    return Common.to_json('success', item)


@user.route('/addPermission', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def addPermission():
    userId = request.json.get('user_id')
    permission = request.json.get('permission')
    uId = Auth.getID()
    creat_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    creator = db.session.query(Users).filter(Users.id == uId).first()
    creatorname = creator.name
    item = Permission(user_id=userId, permission=permission, create_time=creat_time, creator=creatorname)
    db.session.add(item)
    res = db.session.commit()
    return Common.to_json('success')


@user.route('/updatePermission', methods=['post'])
@Auth.require_jwt
@Auth.require_root
def updatePermission():
    id = request.json.get('id')
    permission = request.json.get('permission')
    item = Permission.query.filter_by(id=id).first()
    item.permission = permission
    db.session.add(item)
    result = db.session.commit()
    return Common.to_json('success', dict(data=str(result)))
