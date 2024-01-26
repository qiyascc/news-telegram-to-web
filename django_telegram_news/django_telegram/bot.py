from pyrogram import Client, filters
from datetime import datetime
import os
import json
import requests

api_id = ur_api_id
api_hash = 'ur_api_hash'
bot_token = 'ur_bot_token'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def update_central_data(user_id, data, file_path="data.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_data = json.load(file)
    else:
        all_data = {}

    if user_id not in all_data:
        all_data[user_id] = []

    all_data[user_id].append(data)

    with open(file_path, "w") as file:
        json.dump(all_data, file, indent=4)
    
    try:
        response = requests.get('http://127.0.0.1:8000/api/news/', json=all_data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API isteğinde hata: {e}")


@app.on_message(filters.group)
def handle_message(client, message):
    user_id = message.from_user.id
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    media_path = None
    text_content = message.caption or message.text or ""

    if message.photo:
        photo_extension = "jpg"
        media_folder = f"./messages/{user_id}/{timestamp}"
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)
        media_path = f"{media_folder}/photo.{photo_extension}"
        message.download(media_path)

    data = {
        timestamp: {
            "pic": media_path,
            "text": text_content
        }
    }

    update_central_data(str(user_id), data)

app.run()