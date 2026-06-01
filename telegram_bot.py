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

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict):
    data = [data]

# Load last uploaded ID
try:
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
        last_uploaded_id = str(state.get("last_uploaded_id", ""))
except:
    last_uploaded_id = ""

# Find start position
start_index = 0

if last_uploaded_id:
    for i, item in enumerate(data):
        if str(item.get("id")) == last_uploaded_id:
            start_index = i + 1
            break

# Restart from beginning if end reached
if start_index >= len(data):
    start_index = 0

# Get next posts
posts = data[start_index:start_index + POSTS_PER_DAY]

# If less than 10 remain, continue from beginning
if len(posts) < POSTS_PER_DAY:
    remaining = POSTS_PER_DAY - len(posts)
    posts.extend(data[:remaining])

print(f"Starting Index: {start_index}")
print(f"Posting {len(posts)} prompts")

post_count = 0
last_successful_id = None

for item in posts:
    try:
        item_id = str(item.get("id", ""))
        title = item.get("title", "")
        prompt = item.get("prompt", "")
        image_url = item.get("image_url", "")

        if not image_url:
            print(f"Skipped {item_id} - No image")
            continue

        # Send image
        photo_payload = {
            "chat_id": CHANNEL_ID,
            "photo": image_url,
            "caption": title[:1024],
            "parse_mode": "HTML"
        }

        photo_response = requests.post(
            PHOTO_URL,
            data=photo_payload,
            timeout=30
        )

        if photo_response.status_code != 200:
            print(f"Image Failed {item_id}: {photo_response.text}")
            continue

        print(f"Image Posted: {item_id}")

        time.sleep(2)

        # Send prompt
        text_payload = {
            "chat_id": CHANNEL_ID,
            "text": prompt[:4096],
            "parse_mode": "HTML"
        }

        text_response = requests.post(
            MESSAGE_URL,
            data=text_payload,
            timeout=30
        )

        if text_response.status_code != 200:
            print(f"Prompt Failed {item_id}: {text_response.text}")
            continue

        print(f"Prompt Posted: {item_id}")

        last_successful_id = item_id
        post_count += 1

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
        print(f"Error {item.get('id')}: {e}")

# Save last uploaded ID
if last_successful_id:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "last_uploaded_id": last_successful_id
            },
            f,
            indent=4
        )

    print(f"Saved last_uploaded_id: {last_successful_id}")

print("Done")
