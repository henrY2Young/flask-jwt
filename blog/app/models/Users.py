from app import db
from werkzeug.security import check_password_hash, generate_password_hash

class Users(db.Model):
    __tablename__ =  'users'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64),nullable=False,unique=True)
    password_hash = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(64),nullable=False)
    tel = db.Column(db.String(11),nullable=False)
    add_time = db.Column(db.DateTime,nullable=False)
    role = db.Column(db.INTEGER,nullable=False,default=0)

    @property
    def password(self):
        raise AttributeError(u'文明密码不可读')

    # 写入密码，同时计算hash值，保存到模型中
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value, method='pbkdf2:sha1', salt_length=8)

    # 检查密码是否正确
    def check_login_password(self, password):
        return check_password_hash(self.password_hash, password)







