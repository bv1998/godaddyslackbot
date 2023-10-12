import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
import requests
import ssl
from dotenv import load_dotenv

ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()


app = Flask(__name__)

slack_token = os.environ.get('SLACK_API_TOKEN')
slack_client = WebClient(token=slack_token)

channel_id = os.environ.get('SLACK_CHANNEL_ID')
channel_id = '#' + channel_id
godaddy_api_key = os.environ.get('GODADDY_API_KEY')
godaddy_api_secret = os.environ.get('GODADDY_API_SECRET')

@app.route('/nameservers_change', methods=['POST'])
def nameservers_change():
    data = request.json
    domain_name = data['domain_name']
    old_nameservers = data['old_nameservers']
    new_nameservers = data['new_nameservers']
    message = f"Nameservers changed for {domain_name}:\nOld Nameservers: {', '.join(old_nameservers)}\nNew Nameservers: {', '.join(new_nameservers)}"

    slack_client.chat_postMessage(channel=channel_id, text=message)

    return 'OK', 200

@app.route('/transfer_in', methods=['POST'])
def transfer_in():
    data = request.json
    domain_name = data['domain_name']
    message = f"Domain transferred in: {domain_name}"

    slack_client.chat_postMessage(channel=channel_id, text=message)

    return 'OK', 200

@app.route('/transfer_out', methods=['POST'])
def transfer_out():
    data = request.json
    domain_name = data['domain_name']
    message = f"Domain transferred out: {domain_name}"

    slack_client.chat_postMessage(channel=channel_id, text=message)

    return 'OK', 200

@app.route('/renewal', methods=['POST'])
def domain_renewal():
    data = request.json

    if data['event'] == 'domain_renewal':
        domain_name = data['domain_name']
        renewal_period = data['renewal_period']  # Optionally, you can get the renewal period

        message = f"Domain renewal for {domain_name}. Renewal period: {renewal_period} years."

        slack_client.chat_postMessage(channel=channel_id, text=message)

        return 'OK', 200

    return 'Not a domain renewal event', 200

if __name__ == '__main__':
    startup_message = "Notifications for Godaddy have started running."
    slack_client.chat_postMessage(channel=channel_id, text=startup_message)

    app.run(host='0.0.0.0', port=8000)
