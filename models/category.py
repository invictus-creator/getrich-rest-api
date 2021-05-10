import sqlite3
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

    # def update_transaction_prices(self):
    #     conn = sqlite3.connect('data.db')
    #     cur = conn.cursor()
    #
    #     if self.type == 'Income':
    #         query = "UPDATE Transactions SET price=abs(price) WHERE category=?"
    #         cur.execute(query, (self.name,))
    #         conn.commit()
    #         conn.close()
    #     else:
    #         query = "UPDATE Transactions SET price=abs(price)*-1 WHERE category=?"
    #         cur.execute(query, (self.name,))
    #
    #         conn.commit()
    #         conn.close()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # self.update_transaction_prices()
