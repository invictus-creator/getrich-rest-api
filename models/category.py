from db import db


class CategoryModel(db.Model):
    """
    This is the parent to the TransactionModel.
    """
    __tablename__ = 'Categories'
    name = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text)

    def __init__(self, name, _type):
        self.name = name
        self.type = _type

    def json(self):
        return {"name": self.name, "type": self.type}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
