from app import db
class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.String(5), nullable=False, default='')
    permission = db.Column(db.String(100), nullable=False, default='')
    create_time = db.Column(db.DateTime, nullable=False)
    creator = db.Column(db.String(5), nullable=False)
