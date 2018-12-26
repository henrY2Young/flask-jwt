from app import db
class auth(db.Model):
    __tablename__ =  'auth'
    id = db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    user_id = db.Column(db.INTEGER,nullable=False,)
    add_time = db.Column(db.String(64),nullable=False,default='')
    update_time = db.Column(db.String(64),nullable=False,default='')
    authorization = db.Column(db.String(250),nullable=False,default='')
    refresh_code = db.Column(db.String(250), nullable=False,default='')