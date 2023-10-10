import os
from flask import Flask, request
from slack_sdk import WebClient
from godaddypy import Client, Account
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

slack_token = os.environ.get('SLACK_API_TOKEN')
slack_client = WebClient(token=slack_token)

channel_id = os.environ.get('SLACK_CHANNEL_ID')
channel_id = '#' + channel_id
godaddy_api_key = os.environ.get('GODADDY_API_KEY')
godaddy_api_secret = os.environ.get('GODADDY_API_SECRET')

account = Account(api_key=godaddy_api_key, api_secret=godaddy_api_secret)
client = Client(account)

@app.route('/webhook/godaddy', methods=['POST'])
def godaddy_webhook():
    data = request.json

    if data['event'] == 'domain_transfer_in':
        domain_name = data['domain_name']
        message = f"Domain transferred in: {domain_name}"

    elif data['event'] == 'domain_transfer_out':
        domain_name = data['domain_name']
        message = f"Domain transferred out: {domain_name}"

    else:
        message = "Unknown event received from GoDaddy"

    slack_client.chat_postMessage(channel=channel_id, text=message)

    return 'OK', 200

if __name__ == '__main__':
    startup_message = "Flask app for GoDaddy webhook is running."
    slack_client.chat_postMessage(channel=channel_id, text=startup_message)

    app.run(host='0.0.0.0', port=8000)
