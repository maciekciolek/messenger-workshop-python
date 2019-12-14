import random
import requests
from flask import Flask, request

app = Flask(__name__)
ACCESS_TOKEN = ''
VERIFY_TOKEN = ''


def respond(recipient_id, payload):
    body = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': recipient_id
        },
        'message': payload
    }

    response = requests.post(
        'https://graph.facebook.com/v5.0/me/messages?access_token='+ACCESS_TOKEN,
        json=body
    )

    return response.json()


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


@app.route("/", methods=['GET'])
def verify_message():
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)


@app.route("/", methods=['POST'])
def handle_webhook():
    output = request.get_json()
    data = output['entry'][0]['messaging'][0]
    sender_id = data['sender']['id']
    message = data['message']
    if message['text']:
        respond(sender_id, {'text': 'Hej!'})

    return 'ok'


if __name__ == "__main__":
    app.run()
