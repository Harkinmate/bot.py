import feedparser
import requests
import time

# === CONFIG ===
BOT_TOKEN = "7839637427:AAE0LL7xeUVJiJusSHaHTOGYAI3kopwxdn4"
CHANNEL_ID = "@football1805"  # your channel username
RSS_FEED = "https://news.google.com/rss/search?q=football&hl=en-US&gl=US&ceid=US:en"

# Track posted links
posted = set()

def get_feed():
    return feedparser.parse(RSS_FEED).entries

def send_to_telegram(title, link, summary, image_url=None):
    text = f"📰 <b>{title}</b>\n\n{summary}\n\n<a href='{link}'>Read more</a>"
    if image_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": CHANNEL_ID,
            "caption": text,
            "parse_mode": "HTML",
            "photo": image_url
        }
        requests.post(url, data=data)
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        requests.post(url, data=data)

def extract_image(entry):
    # Google News RSS often uses media_content or media_thumbnail
    if "media_content" in entry:
        return entry.media_content[0]["url"]
    if "media_thumbnail" in entry:
        return entry.media_thumbnail[0]["url"]

    # Sometimes links contain image
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
                summary = entry.summary[:400] + "..." if len(entry.summary) > 400 else entry.summary
                send_to_telegram(entry.title, entry.link, summary, img)
                print("Posted:", entry.title)
        time.sleep(20)  # update every 20 seconds

if __name__ == "__main__":
    print("Bot started. Fetching Google News every 20 seconds...")
    run_bot()
