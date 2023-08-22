import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token.
bot_token = "6376673556:AAFUw21pWQ3vPv1BZLDtl2_Xf23iMEmYFLA"
base_url = f"https://api.telegram.org/bot{bot_token}/"

def get_chat_id(update):
    return update["message"]["chat"]["id"]

def read_msg(update):
    message_text = update["message"].get("text")
    chat_id = get_chat_id(update)
    if message_text:
        recording_id = re.search(r'recordingId=(\d+)', message_text)
        if recording_id:
            v = recording_id.group(1)
            send_msg(chat_id, f"https://static.smpopular.com/production/uploading/recordings/{v}/master.mp4")
        else:
            send_msg(chat_id, "Invalid or missing recording ID. Please provide a valid link.")

def send_msg(chat_id, text):
    if chat_id:
        parameter = {
            "chat_id": chat_id,
            "text": text if text else "This URL will not exist. Please check it."
        }
        resp = requests.post(base_url + "sendMessage", data=parameter)

@app.route("/webhook", methods=["POST","GET"])
def webhook():
    if request.method == "POST":
        update = request.json
        read_msg(update)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
