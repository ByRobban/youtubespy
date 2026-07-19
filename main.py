import os
import requests
from googleapiclient.discovery import build
import pandas as pd

# Secrets'tan gelen veriler
API_KEY = os.environ['API_KEY']
TG_TOKEN = os.environ['TG_TOKEN']
TG_ID = os.environ['TG_ID']

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_ID, "text": message}
    requests.post(url, data=payload)

def get_trends():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode="TR",
        maxResults=50
    )
    response = request.execute()
    
    # Sadece kategori ID'lerini topla
    categories = [item['snippet']['categoryId'] for item in response['items']]
    df = pd.Series(categories).value_counts().to_string()
    return f"📊 Haftalık Trend Özeti (Kategori ID'lerine göre):\n\n{df}"

if __name__ == "__main__":
    try:
        report = get_trends()
        send_telegram(report)
    except Exception as e:
        send_telegram(f"Hata oluştu: {str(e)}")
