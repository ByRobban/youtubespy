import os
import requests
from googleapiclient.discovery import build

# Secrets
API_KEY = os.environ['API_KEY']
TG_TOKEN = os.environ['TG_TOKEN']
TG_ID = os.environ['TG_ID']

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    # Uzun mesajları parçalamak için parse_mode=Markdown ekleyebiliriz
    requests.post(url, data={"chat_id": TG_ID, "text": message, "parse_mode": "Markdown"})

def get_trends():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    # 20 tane trend videoyu çek
    response = youtube.videos().list(
        part="snippet", 
        chart="mostPopular", 
        regionCode="TR", 
        maxResults=20
    ).execute()
    
    msg = "🔥 *Şu Anki Trend Videolar (İlk 20):*\n\n"
    for i, item in enumerate(response['items'], 1):
        title = item['snippet']['title']
        video_id = item['id']
        link = f"https://www.youtube.com/watch?v={video_id}"
        # Markdown formatında liste oluşturuyoruz
        msg += f"{i}. [{title}]({link})\n"
    
    return msg

if __name__ == "__main__":
    try:
        send_telegram(get_trends())
    except Exception as e:
        send_telegram(f"Hata oluştu: {str(e)}")
