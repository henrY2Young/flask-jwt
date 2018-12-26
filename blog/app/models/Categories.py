from app import db


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False, default=0)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
