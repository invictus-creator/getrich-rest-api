from db import db
# from sqlalchemy import func
# from sqlalchemy.ext.hybrid import hybrid_property


class TransactionModel(db.Model):
    """
    This is a child of the CategoryModel.
    """
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    vendor = db.Column(db.Text)
    category = db.Column(db.Text, db.ForeignKey('Categories.name'))
    price = db.Column(db.Float(precision=2))

    # @hybrid_property
    # def positive_price(self):
    #     return abs(self.price)
    #
    # @positive_price.expression
    # def positive_price(cls):
    #     return func.abs(cls.price)
    #
    # @hybrid_property
    # def negative_price(self):
    #     return abs(self.price)*-1
    #
    # @positive_price.expression
    # def negative_price(cls):
    #     return func.abs(cls.price)*-1

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
            db.session.query(cls).filter(cls.category == name).update({cls.price: abs(cls.price)})
        else:
            db.session.query(cls).filter(cls.category == name).update({cls.price: abs(cls.price)*-1})

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    #     if _type == "Income":
    #         # cls.query.update(price=abs(cls.c.price)).where(cls.c.category == name)
    #         db.update(cls).where(cls.category == name).values(price=cls.positive_price)
    #         # cls.query.update().where(cls.c.category == name).values(price=abs(cls.c.price))
    #         db.session.commit()
    #     else:
    #         # cls.query.update(price=abs(cls.c.price)*-1).where(cls.c.category == name)
    #         db.update(cls).where(cls.category == name).values(price=cls.negative_price)
    #         # cls.query.update().where(cls.c.category == name).values(price=abs(cls.c.price)*-1)
    #         db.session.commit()