import json
import requests
import time
import random

BOT_TOKEN = "8730206290:AAG-5VW7cfsh0gPvElLjdq9B6KMnlsbQqk8"
CHANNEL_ID = "-1003806372069"

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict):
    data = [data]

post_count = 0

# 🔥 CTA LIST (random rotation)
cta_list = [
    """🔻🔻🔻👇👇👇🔻🔻🔻
🔥 2000+ AI Image Prompts Ready

Create scroll-stopping images in seconds  
No skills. No effort.

👇 Try now  
https://play.google.com/store/apps/details?id=com.aipromptcollection.app""",

    """🔻🔻🔻👇👇👇🔻🔻🔻
⚡ Make Viral AI Images Fast

2000+ ready prompts inside  
Just copy & generate

👇 Download now  
https://play.google.com/store/apps/details?id=com.aipromptcollection.app""",

    """🔻🔻🔻👇👇👇🔻🔻🔻
𝟮𝟬𝟬𝟬+ 𝗡𝗲𝘄 𝗣𝗿𝗼𝗺𝗽𝘁𝘀 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗱 𝗼𝗻 𝗢𝘂𝗿 𝗔𝗽𝗽 ✅

Don’t miss out on the latest trending prompts  
Create viral AI images instantly

👇 Download Now  
https://play.google.com/store/apps/details?id=com.aipromptcollection.app"""
]

PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

for i, item in enumerate(data):
    try:
        item_id = item.get("id", "")
        title = item.get("title", "")
        prompt = item.get("prompt", "")
        image_url = item.get("image_url", "")
        category = item.get("category_name", "")

        if not image_url:
            print(f"{i+1} Skipped: No image_url")
            continue

        # 📸 Send Image
        payload_photo = {
            "chat_id": CHANNEL_ID,
            "photo": image_url,
            "caption": title or "",
            "parse_mode": "HTML"
        }

        res1 = requests.post(PHOTO_URL, data=payload_photo)

        if res1.status_code != 200:
            print(f"{item_id} Image Failed:", res1.text)
            continue

        print(f"{item_id} Posted Image")

        # 📝 Send Prompt
        payload_text = {
            "chat_id": CHANNEL_ID,
            "text": prompt,
            "parse_mode": "HTML"
        }

        res2 = requests.post(MESSAGE_URL, data=payload_text)

        if res2.status_code != 200:
            print(f"{item_id} Caption Failed:", res2.text)
        else:
            print(f"{item_id} Posted Caption")

        post_count += 1

        # ⏱️ Normal delay
        time.sleep(2)

        # 🛑 After every 8 posts → wait + send CTA
        if post_count % 4 == 0:
            print("⏸️ Waiting 5 seconds after 4 posts...")

            random_cta = random.choice(cta_list)

            payload_cta = {
                "chat_id": CHANNEL_ID,
                "text": random_cta,
                "parse_mode": "HTML"
            }

            res3 = requests.post(MESSAGE_URL, data=payload_cta)

            if res3.status_code != 200:
                print("CTA Failed:", res3.text)
            else:
                print("CTA Sent Successfully")

            time.sleep(5)


    except Exception as e:
        print(f"{item_id} Error:", e)
