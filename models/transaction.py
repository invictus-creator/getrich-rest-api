from db import db
from sqlalchemy import func


class TransactionModel(db.Model):
    """
    This is a child of the CategoryModel.
    """
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    vendor = db.Column(db.Text)
    category = db.Column(db.Text)
    price = db.Column(db.Float(precision=2))

    def __init__(self, date, vendor, category, price):
        self.date = date
        self.vendor = vendor
        self.category = category
        self.price = price

    def json(self):
        return {"id": self.id, "date": self.date, "vendor": self.vendor, "category": self.category, "price": self.price}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def update_prices(cls, name, _type):
        if _type == "Income":
            db.session.query(cls).filter(cls.category == name).update({cls.price: func.abs(cls.price)})
        else:
            db.session.query(cls).filter(cls.category == name).update({cls.price: func.abs(cls.price) * -1})

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
