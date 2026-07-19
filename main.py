import os
import requests
from googleapiclient.discovery import build
import pandas as pd

# Secrets
API_KEY = os.environ['API_KEY']
TG_TOKEN = os.environ['TG_TOKEN']
TG_ID = os.environ['TG_ID']

# Kategori Sözlüğü (ID -> İsim)
CATEGORIES = {
    "1": "Film & Animasyon", "2": "Otolar", "10": "Müzik", "15": "Hayvanlar",
    "17": "Spor", "19": "Seyahat", "20": "Oyun", "22": "Blog", "23": "Komedi",
    "24": "Eğlence", "25": "Haber", "26": "Nasıl Yapılır", "27": "Eğitim",
    "28": "Teknoloji", "29": "STK"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TG_ID, "text": message})

def get_trends():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    response = youtube.videos().list(part="snippet", chart="mostPopular", regionCode="TR", maxResults=50).execute()
    
    # ID'leri isimlerle eşleştir
    cat_names = [CATEGORIES.get(item['snippet']['categoryId'], "Diğer") for item in response['items']]
    
    # Say ve formatla
    df = pd.Series(cat_names).value_counts().to_string()
    return f"🚀 Trend YouTube Kategorileri (TR):\n\n{df}"

if __name__ == "__main__":
    try:
        send_telegram(get_trends())
    except Exception as e:
        send_telegram(f"Hata: {str(e)}")
