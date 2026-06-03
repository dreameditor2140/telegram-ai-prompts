import json
import requests
import time
import random
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

POSTS_PER_RUN = 10

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

if not data:
    print("No prompts remaining.")
    exit()

# Take first 10 records
posts = data[:POSTS_PER_RUN]

print(f"Loaded {len(data)} prompts")
print(f"Posting {len(posts)} prompts")

successful_ids = []
post_count = 0

for item in posts:
    try:
        item_id = str(item.get("id", ""))
        title = item.get("title", "")
        prompt = item.get("prompt", "")
        image_url = item.get("image_url", "")

        if not image_url:
            print(f"Skipped {item_id} - No image")
            continue

        # Send Image
        photo_response = requests.post(
            PHOTO_URL,
            data={
                "chat_id": CHANNEL_ID,
                "photo": image_url,
                "caption": title[:1024],
                "parse_mode": "HTML"
            },
            timeout=60
        )

        if photo_response.status_code != 200:
            print(f"Image Failed {item_id}")
            print(photo_response.text)
            continue

        print(f"Image Posted: {item_id}")

        time.sleep(2)

        # Send Prompt
        text_response = requests.post(
            MESSAGE_URL,
            data={
                "chat_id": CHANNEL_ID,
                "text": prompt[:4096],
                "parse_mode": "HTML"
            },
            timeout=60
        )

        if text_response.status_code != 200:
            print(f"Prompt Failed {item_id}")
            print(text_response.text)
            continue

        print(f"Prompt Posted: {item_id}")

        successful_ids.append(item_id)
        post_count += 1

        # CTA after every 4 posts
        if post_count % 4 == 0:
            cta = random.choice(cta_list)

            cta_response = requests.post(
                MESSAGE_URL,
                data={
                    "chat_id": CHANNEL_ID,
                    "text": cta
                },
                timeout=60
            )

            if cta_response.status_code == 200:
                print("CTA Sent")

        time.sleep(5)

    except Exception as e:
        print(f"Error {item.get('id')}: {e}")

# Remove uploaded records
if successful_ids:

    updated_data = [
        item
        for item in data
        if str(item.get("id")) not in successful_ids
    ]

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(
            updated_data,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"Removed {len(successful_ids)} uploaded prompts")
    print(f"Remaining prompts: {len(updated_data)}")

print("Done")
