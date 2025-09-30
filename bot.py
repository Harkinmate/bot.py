import feedparser
import requests
import time

# === CONFIG ===
BOT_TOKEN = "7839637427:AAE0LL7xeUVJiJusSHaHTOGYAI3kopwxdn4"
CHANNEL_ID = "@football1805"  # your channel username
RSS_FEED = "http://feeds.bbci.co.uk/sport/football/rss.xml"

# Track posted links
posted = set()

def get_feed():
    return feedparser.parse(RSS_FEED).entries

def send_to_telegram(title, link, summary, image_url=None):
    text = f"📰 <b>{title}</b>\n\n{summary}\n"
    if image_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {"chat_id": CHANNEL_ID, "caption": text, "parse_mode": "HTML"}
        files = {"photo": requests.get(image_url).content}
        requests.post(url, data=data, files=files)
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
        requests.post(url, data=data)

def extract_image(entry):
    if "media_content" in entry:
        return entry.media_content[0]["url"]
    if "links" in entry:
        for l in entry.links:
            if l.get("type", "").startswith("image"):
                return l["href"]
    return None

def run_bot():
    global posted
    while True:
        feed = get_feed()
        for entry in feed[:5]:  # check latest 5
            if entry.link not in posted:
                posted.add(entry.link)
                img = extract_image(entry)
                send_to_telegram(entry.title, entry.link, entry.summary, img)
                print("Posted:", entry.title)
        time.sleep(300)  # wait 5 mins before checking again

if __name__ == "__main__":
    run_bot()
