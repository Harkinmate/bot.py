import feedparser
import json
import time
from newspaper import Article
from telegram import Bot
from telegram.error import TelegramError

# ---------------- CONFIG ----------------
BOT_TOKEN = "7839637427:AAE0LL7xeUVJiJusSHaHTOGYAI3kopwxdn4"
CHANNEL_ID = "@football1805"
RSS_URL = "http://feeds.bbci.co.uk/sport/football/rss.xml"
POSTED_FILE = "posted_links.json"
FETCH_LIMIT = 5         # number of latest articles per run
SLEEP_SECONDS = 20      # update every 20 seconds
# ---------------------------------------

bot = Bot(token=BOT_TOKEN)

# Load posted links
try:
    with open(POSTED_FILE, "r") as f:
        posted_links = set(json.load(f))
except:
    posted_links = set()

def save_posted_links():
    with open(POSTED_FILE, "w") as f:
        json.dump(list(posted_links), f)

def get_main_image(url):
    """Get high-quality image from article"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.top_image if article.top_image else None
    except Exception as e:
        print("Image scrape failed:", e)
        return None

def fetch_and_post():
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries[:FETCH_LIMIT]:
        if entry.link in posted_links:
            continue

        title = entry.title
        summary = entry.summary[:400] + "..." if len(entry.summary) > 400 else entry.summary
        url = entry.link

        image_url = get_main_image(url)

        try:
            if image_url:
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image_url,
                    caption=f"📰 {title}\n\n{summary}\n\nRead more: {url}"
                )
            else:
                bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=f"📰 {title}\n\n{summary}\n\nRead more: {url}"
                )
            print(f"Posted: {title}")
        except TelegramError as e:
            print("Telegram error:", e)

        posted_links.add(url)
        save_posted_links()

if __name__ == "__main__":
    print("Bot started. Fetching articles every 20 seconds...")
    while True:
        try:
            fetch_and_post()
        except Exception as e:
            print("Error in fetch_and_post:", e)
        time.sleep(SLEEP_SECONDS)
