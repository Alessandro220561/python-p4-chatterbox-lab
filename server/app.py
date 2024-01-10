from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>ChatterBox-API</h1>'

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(asc(Message.created_at))]

        return jsonify(messages), 200
    
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_message = Message(
                body=data.get('body'),
                username=data.get('username')
            )

        db.session.add(new_message)
        db.session.commit()

        new_message_serialized = new_message.to_dict()

        return jsonify(new_message_serialized), 200

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'GET':
        message_dict = message.to_dict()
        return jsonify(message_dict), 200
    
    elif request.method == 'PATCH':
        if request.is_json:
            data = request.get_json()
            for attr, value in data.items():
                setattr(message, attr, value)

            db.session.commit()

            message_serialized = message.to_dict()

            return jsonify(message_serialized), 200
        
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            'delete_succesful': True,
            'message': 'Message deleted'
        }

        return jsonify(response_body), 200

if __name__ == '__main__':
    app.run(port=5555)
