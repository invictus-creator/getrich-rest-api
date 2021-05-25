from db import db

class NotificationModel(db.Model):
    """NotificationModel is the model for Notification resource.

        -- tablename: Notifications
        -- Columns:
            - id (integer, primary key)
            - date (DateTime, formatted as %Y-%m-%d)
            - description (text)
            - price (float, with 2 decimal places)
            - state (integer, 0 for off and 1 for on)

    Methods:
        json: returns json representaion of itself
        find_by_id: finds and returns the NotificationModel object with specified id
        save_to_db:
        delete_from_db:
    """
    __tablename__ = 'Notifications'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    price = db.Column(db.Float(precision=2))
    state = db.Column(db.Integer)

    def __init__(self, date, description, price, state):
        self.date = date
        self.description = description
        self.price = price
        self.state = state

    def json(self):
        return {"id": self.id,
                "date": self.date.strftime("%Y-%m-%d"),
                "description": self.description,
                "price": self.price,
                "state": self.state}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
