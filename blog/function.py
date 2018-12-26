from flask import json


class Common:
    @staticmethod
    def to_json(status='success', data=[]):
        if not ErrorCode[status]:
            return json.dumps(dict(msg='status not found'))
        return json.dumps(dict(code=ErrorCode[status], msg=status, data=data))


ErrorCode = {
    'not_found': 404,
    'success': 1000,
    'error': -1000,
    'timeout': 502502,
    'timeerror':502501
}
