from datetime import datetime

# from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.notification import NotificationModel
from db import db


class Notification(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=False)
    parser.add_argument('date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('state',
                        type=int,
                        required=True,
                        help="This field cannot be left blank. 0 for off, 1 for on.")

    # @jwt_required()
    def get(self):

        data = Notification.parser.parse_args()
        notification = NotificationModel.find_by_id(data['id'])

        if notification:
            return notification.json(), 200
        else:
            return {"message": "Notification not found."}, 404

    # @jwt_required()
    def post(self):
        data = Notification.parser.parse_args()

        notification = NotificationModel(datetime.strptime(data['date'], "%Y-%m-%d"),
                                         data['description'].lower(),
                                         data['price'],
                                         data['state'])

        try:
            notification.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the notification. {e}"}, 500

        return notification.json()

    # @jwt_required()
    def put(self):
        data = Notification.parser.parse_args()

        notification = NotificationModel.find_by_id(data['id'])

        if notification is None:
            notification = NotificationModel(datetime.strptime(data['date'], "%Y-%m-%d"),
                                             data['description'].lower(),
                                             data['price'],
                                             data['state'])
        else:
            notification.date = datetime.strptime(data['date'], "%Y-%m-%d")
            notification.description = data['description'].lower()
            notification.price = data['price']
            notification.state = data['state']
        try:
            notification.save_to_db()
        except:
            return {"message": "An error occurred inserting/updating the notification."}, 500

        return notification.json()

    # @jwt_required()
    def delete(self):
        data = Notification.parser.parse_args()

        notification = NotificationModel.find_by_id(data['id'])
        if notification:
            notification.delete_from_db()

        return {"message": "Notification deleted."}


class NotificationList(Resource):
    def get(self):
        return {"notification list": [notification.json() for notification in NotificationModel.query.all()], }
