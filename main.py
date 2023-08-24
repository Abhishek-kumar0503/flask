import requests
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token.
bot_token = "6376673556:AAFUw21pWQ3vPv1BZLDtl2_Xf23iMEmYFLA"
base_url = f"https://api.telegram.org/bot{bot_token}/"


def get_chat_id(update):
    return update["message"]["chat"]["id"]

def read_msg(offset):
    parameter = {
        "offset": offset
    }
    resp = requests.get(base_url + "getUpdates", params=parameter)
    data = resp.json()

    for result in data["result"]:
        message = result.get("message", {}).get("text")
        chat_id = get_chat_id(result)
        if message and is_valid_url(message):
            response = requests.get(message)
            message_text = response.url
            recording_id = re.search(r'recordingId=(\d+)', message_text)
            if recording_id:
                v = recording_id.group(1)
                video_url = f"https://static.smpopular.com/production/uploading/recordings/{v}/master.mp4"
                send_video(chat_id, video_url)
        else:
            send_msg(chat_id, "Invalid or missing recording ID. Please provide a valid link.")

    if "result" in data and data["result"]:
        return data["result"][-1]["update_id"] + 1

def send_msg(chat_id, text):
    if chat_id:
        parameter = {
            "chat_id": chat_id,
            "text": text if text else "This URL will not exist. Please check it."
        }
        requests.post(base_url + "sendMessage", data=parameter)

def send_video(chat_id, video_url):
    if chat_id:
        parameter = {
            "chat_id": chat_id,
        }
        files = {
            "video": requests.get(video_url).content
        }
        resp = requests.post(base_url + "sendVideo", data=parameter, files=files)

def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

@app.route("/webhook", methods=["POST","GET"])
def webhook():
    if request.method == "POST":
        update = request.json
        read_msg(update)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
