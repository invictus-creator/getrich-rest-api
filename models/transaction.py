from db import db
from sqlalchemy import func


class TransactionModel(db.Model):
    """TransactionModel is the model class for the Transaction resource.

        -- tablename: Transactions
        -- Columns:
            - id (integer, primary key)
            - date (text, formatted as %Y-%m-%d)
            - vendor (text)
            - category (text)
            - price (float, with 2 decimal places)

    Methods:
        json: returns json representaion of itself
        find_by_id: finds and returns the TransactionModel object with specified id
        update_prices: class method, changes the price's sign for each row with given category name, depending
                        on the given type ("income", "expense")
        save_to_db:
        delete_from_db:
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
    def update_prices(cls, name, type):
        if type == "income":
            db.session.query(cls).filter(cls.category == name).update({cls.price: func.abs(cls.price)})
        elif type == "expense":
            db.session.query(cls).filter(cls.category == name).update({cls.price: func.abs(cls.price) * -1})

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
