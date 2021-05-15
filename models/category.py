from db import db

class CategoryModel(db.Model):
    """TransactionModel is the model class for the Transaction resource.

        -- tablename: Categories
        -- Columns:
            - id (integer, primary key)
            - name (text, unique constraint)
            - type: (text)

    Methods:
        json: returns json representaion of itself
        find_by_name: finds and returns the CategoryModel object with specified name
        save_to_db:
        delete_from_db:
    """
    __tablename__ = 'Categories'
    __table_args__ = (db.UniqueConstraint("name"),)
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    db.UniqueConstraint("")

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def json(self):
        return {"name": self.name, "type": self.type}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
