from flask import jsonify
from flask_restful import Resource, reqparse, abort

from data import db_session
from data.users import Purchases


def abort_if_purchases_not_found(purchases_id):
    session = db_session.create_session()
    purchases = session.query(Purchases).get(purchases_id)
    if not purchases:
        abort(404, message=f"Purchases {purchases_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('count', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('id', required=True, type=int)


class PurchasesResource(Resource):
    def get(self, purchases_id):
        abort_if_purchases_not_found(purchases_id)
        session = db_session.create_session()
        purchases = session.query(Purchases).get(purchases_id)
        return jsonify({'purchases': purchases.to_dict(
            only=('title', 'content', 'count', 'user_id',))})

    def delete(self, purchases_id):
        abort_if_purchases_not_found(purchases_id)
        session = db_session.create_session()
        purchases = session.query(Purchases).get(purchases_id)
        session.delete(purchases)
        session.commit()
        return jsonify({'success': 'OK'})


class PurchasesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        purchases = session.query(Purchases).all()
        return jsonify({'purchases': [item.to_dict(
            only=('id', 'title', 'content', 'count', 'user_id',)) for item in purchases]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        purchases = Purchases(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            count=args['count'],
        )
        session.add(purchases)
        session.commit()
        return jsonify({'success': 'OK'})
