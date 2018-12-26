import hashlib
from functools import wraps

from app.models.Users import Users
from app.models.Auth import auth
from app.models.Permission import Permission
from app.models.Categories import Categories
import jwt, datetime, time
from flask import request, g
from app import db
from config import Config


class Auth():
    @staticmethod
    def encode_jwt(user_id, login_time):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=15 * 60 * 60),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_jwt(auth_token):
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': True})
            if ('data' in payload and 'id' in payload['data']):
                return dict(payload=payload['data'], code=1000, msg='success')
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return dict(payload=dict(id=''), code=502502, msg='timeout')
        except jwt.InvalidTokenError:
            return dict(payload=dict(id=''), code=-1000, msg='无效token')

    @staticmethod
    def generate_refresh_token(token):
        refresh_code = hashlib.md5(token).hexdigest()
        return refresh_code

    @staticmethod
    def generate_jwt(user_id, login_time, saveTodb=True):
        token = (Auth.encode_jwt(user_id, login_time))
        refresh_token = Auth.generate_refresh_token(token)
        if saveTodb:
            updata_time = int(time.time())
            item = auth(user_id=user_id, add_time=login_time, update_time=updata_time,
                        authorization=str(token, encoding='utf-8'),
                        refresh_code=refresh_token)
            db.session.add(item)
            result = db.session.commit()
            if result == None:
                return dict(jwt=str(token, encoding='utf-8'), refresh_token=refresh_token)
        return dict(jwt=str(token, encoding='utf-8'), refresh_token=refresh_token)

    @staticmethod
    def get_jwt_by_refresh_code(refresh_code):
        auth_info = db.session.query(auth).filter(auth.refresh_code == refresh_code,
                                                  auth.authorization == g.authorization).first()
        if auth_info is None:
            return (dict(code=-1000, msg='not found'))
        if int(time.time()) - int(auth_info.update_time) < 15 * 60:
            return (dict(code=-502501, msg='time error'))
        if int(time.time()) - int(auth_info.update_time) > 60 * 60 * 12:
            return (dict(code=502502, msg='timeout'))
        user_info = db.session.query(Users).filter(Users.id == auth_info.user_id).first()
        login_time = int(time.time())
        result = Auth.generate_jwt(user_id=user_info.id, login_time=login_time, saveTodb=False)
        if auth_info:
            auth_info.update_time = login_time
            auth_info.authorization = result['jwt']
            auth_info.refresh_code = result['refresh_token']
            db.session.add(auth_info)
            db.session.commit()
            return dict(jwt=(result['jwt']), refresh_token=result['refresh_token'])

    @staticmethod
    def getUserId():
        authorization = g.authorization
        if authorization is None:
            return 'need token'
        else:
            res = Auth.decode_jwt(authorization)
            if res['code'] and res['code'] == 1000:
                return res
            else:
                return res

    @staticmethod
    def getID():
        authorization = g.authorization
        if authorization is None:
            return 'need token'
        else:
            res = Auth.decode_jwt(authorization)
            if res['code'] and res['code'] == 1000:
                return res['payload']['id']
            else:
                return res

    @staticmethod
    def permission():
        if g.authorization == '':
            return 'need token'
        userId = Auth.getUserId()
        if userId['code'] == 502502:
            return dict(code=userId['code'], msg='time out', data=[])
        user_id = userId['payload']['id']
        permissionsUrl = []
        menuList = []
        permissions = db.session.query(Permission).filter(Permission.user_id == user_id).first()
        if permissions is None:
            g.url = permissionsUrl
            return dict(code=userId['code'], msg='time out', data=[])
        for ids in (permissions.permission.split(',')):
            categoriesList = db.session.query(Categories).filter(Categories.id == ids).first()
            item = dict(id=ids, name=categoriesList.name, url=categoriesList.url,
                        parentId=categoriesList.parent_id, icon=categoriesList.icon)
            permissionsUrl.append(categoriesList.url)
            menuList.append(item)
        #     return 'permission Forbidden'
        g.url = permissionsUrl
        return dict(code=userId['code'], msg='success', data=dict(menuList=menuList))

    @staticmethod
    def authenticatePermission(url):
        if g.authorization == '':
            return 'need token'
        userId = Auth.getUserId()['payload']['id']
        if userId == '':
            return []
        permissionsUrl = []
        permissions = db.session.query(Permission).filter(Permission.user_id == userId).first()
        if permissions is None:
            return False
        for ids in (permissions.permission.split(',')):
            categoriesList = db.session.query(Categories).filter(Categories.id == ids).first()
            permissionsUrl.append(categoriesList.url)
        for item in permissionsUrl:
            if url == item:
                return True
        return False

    @staticmethod
    def require_jwt(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            authorization = g.authorization
            if authorization is None:
                return 'need token'
            else:
                print("[DEBUG]: enter {}(),Authorization = {}".format(func.__name__, authorization))
                return func()

        return wrapper

    @staticmethod
    def require_root(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ID = Auth.getID()
            try:
                exist = db.session.query(Users).filter(Users.id == ID and Users.role == 1).first()
                if not exist:
                    return 'need root '
                else:
                    return func()
            except Exception as e:
                return 'need root except '

        return wrapper
