import json
import requests
import time
import random
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

POSTS_PER_DAY = 10
STATE_FILE = "state.json"

# CTA Messages
cta_list = [
    """🔻🔻🔻👇👇👇🔻🔻🔻

🔥 2000+ AI Image Prompts Ready

Create scroll-stopping images in seconds
No skills. No effort.

👇 Try now
https://play.google.com/store/apps/details?id=com.aipromptcollection.app
""",

    """🔻🔻🔻👇👇👇🔻🔻🔻

⚡ Make Viral AI Images Fast

2000+ ready prompts inside
Just copy & generate

👇 Download now
https://play.google.com/store/apps/details?id=com.aipromptcollection.app
""",

    """🔻🔻🔻👇👇👇🔻🔻🔻

𝟮𝟬𝟬𝟬+ 𝗡𝗲𝘄 𝗣𝗿𝗼𝗺𝗽𝘁𝘀 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗱 𝗼𝗻 𝗢𝘂𝗿 𝗔𝗽𝗽 ✅

Create viral AI images instantly

👇 Download Now
https://play.google.com/store/apps/details?id=com.aipromptcollection.app
"""
]

# Load prompt data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict):
    data = [data]

# Load state
try:
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
        start_index = state.get("last_index", 0)
except:
    start_index = 0

# Restart from beginning if completed
if start_index >= len(data):
    start_index = 0

posts = data[start_index:start_index + POSTS_PER_DAY]

print(f"Posting {len(posts)} prompts")
print(f"Starting index: {start_index}")

post_count = 0

for item in posts:

    try:
        item_id = item.get("id", "")
        title = item.get("title", "")
        prompt = item.get("prompt", "")
        image_url = item.get("image_url", "")

        if not image_url:
            print(f"Skipped {item_id} - no image")
            continue

        # Send Photo
        photo_payload = {
            "chat_id": CHANNEL_ID,
            "photo": image_url,
            "caption": title,
            "parse_mode": "HTML"
        }

        photo_response = requests.post(
            PHOTO_URL,
            data=photo_payload,
            timeout=30
        )

        if photo_response.status_code != 200:
            print("Photo Failed:", photo_response.text)
            continue

        print(f"Image Posted: {item_id}")

        time.sleep(2)

        # Send Prompt
        text_payload = {
            "chat_id": CHANNEL_ID,
            "text": prompt,
            "parse_mode": "HTML"
        }

        text_response = requests.post(
            MESSAGE_URL,
            data=text_payload,
            timeout=30
        )

        if text_response.status_code == 200:
            print(f"Prompt Posted: {item_id}")
        else:
            print("Prompt Failed:", text_response.text)

        post_count += 1

         time.sleep(2)

        # CTA after every 4 posts
        if post_count % 4 == 0:

            cta = random.choice(cta_list)

            requests.post(
                MESSAGE_URL,
                data={
                    "chat_id": CHANNEL_ID,
                    "text": cta
                },
                timeout=30
            )

            print("CTA Sent")

        time.sleep(5)

    except Exception as e:
        print("Error:", e)

# Save next position
next_index = start_index + len(posts)

with open(STATE_FILE, "w") as f:
    json.dump(
        {
            "last_index": next_index
        },
        f
    )

print("Done")
print("Next Start Index:", next_index)
