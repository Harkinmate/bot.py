import feedparser
import requests
import telegram
import time
from newspaper import Article

# Telegram details
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@football1805"

# RSS feed
RSS_URL = "http://feeds.bbci.co.uk/sport/football/rss.xml"

bot = telegram.Bot(token=BOT_TOKEN)

# Keep track of posted links
posted_links = set()

def get_main_image(url):
    """Scrape article to get high-quality main image"""
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
    for entry in feed.entries[:1]:  # latest only
        if entry.link not in posted_links:
            title = entry.title
            summary = entry.summary[:400] + "..." if len(entry.summary) > 400 else entry.summary
            url = entry.link

            # Get HQ image from article
            image_url = get_main_image(url)

            if image_url:
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image_url,
                    caption=f"📰 {title}\n\n{summary}"
                )
            else:
                bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=f"📰 {title}\n\n{summary}"
                )

            posted_links.add(entry.link)

# Run every 5 minutes
while True:
    fetch_and_post()
    time.sleep(300)
