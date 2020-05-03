# import flask
# from flask import jsonify, request
# from flask_login import current_user
#
# from data import db_session
# from data.users import Purchases
#
# blueprint = flask.Blueprint('purchases_api', __name__,
#                             template_folder='templates')
#
#
# @blueprint.route('/api/purchases')
# def get_purchases():
#     session = db_session.create_session()
#     purchases = session.query(Purchases).all()
#     return jsonify(
#         {
#             'purchases':
#                 [item.to_dict(only=('title', 'count', 'content', 'user.name'))
#                  for item in purchases]
#         }
#     )
#
#
# @blueprint.route('/api/purchases/<int:purchases_id>', methods=['GET'])
# def get_one_purchases(purchases_id):
#     session = db_session.create_session()
#     purchases = session.query(Purchases).get(purchases_id)
#     if not purchases:
#         return jsonify({'error': 'Not found'})
#     return jsonify(
#         {
#             'purchases': purchases.to_dict(only=('title', 'content', 'count', 'user_id',))
#         }
#     )
#
#
# @blueprint.route('/api/purchases', methods=['POST'])
# def create_purchases():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['title', 'content', 'count', 'user_id', ]):
#         return jsonify({'error': 'Bad request'})
#     session = db_session.create_session()
#     purchases = Purchases(
#         title=request.json['title'],
#         content=request.json['content'],
#         count=request.json['count'],
#         user_id=request.json['user_id'],
#     )
#     session.add(purchases)
#     session.commit()
#     return jsonify({'success': 'OK'})
#
#
# @blueprint.route('/api/purchases/<int:purchases_id>', methods=['DELETE'])
# def delete_purchases(purchases_id):
#     session = db_session.create_session()
#     purchases = session.query(Purchases).get(purchases_id)
#     if not purchases:
#         return jsonify({'error': 'Not found'})
#     session.delete(purchases)
#     session.commit()
#     return jsonify({'success': 'OK'})
