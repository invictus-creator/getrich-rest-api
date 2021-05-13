from db import db


class CategoryModel(db.Model):
    """
    This model creates three columns in the database.

        name: The name of the category, stored as text in lowercase.
        type: The type of category, either income or expense, stored in lowercase.
        transactions: A list of dictionarys--instances of the TransactionModel--or an empty dictionary, stored as JSON.

    """
    __tablename__ = 'Categories'
    name = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text)
    transactions = db.Column(db.JSON, nullable=True)

    def __init__(self, name: str, _type: str, transactions=[{},]):
        self.name = name
        self.type = _type
        self.transactions = transactions

    def json(self):
        return {"name": self.name, "type": self.type, "transactions": self.transactions}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
