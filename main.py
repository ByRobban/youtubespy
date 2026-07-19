import os
from googleapiclient.discovery import build
import requests

# Secrets
API_KEY = os.environ['API_KEY']
TG_TOKEN = os.environ['TG_TOKEN']
TG_ID = os.environ['TG_ID']
CHANNEL_ID = os.environ['CHANNEL_ID']

def get_channel_report():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    # Kanal istatistikleri
    res = youtube.channels().list(id=CHANNEL_ID, part='statistics,snippet').execute()
    stats = res['items'][0]['statistics']
    
    # En son yorumlar
    comments = youtube.commentThreads().list(
        allThreadsRelatedToChannelId=CHANNEL_ID, part='snippet', maxResults=3, order='time'
    ).execute()
    
    msg = f"📊 *Günlük Kanal Raporu*\n\n"
    msg += f"👥 Toplam Abone: {stats['subscriberCount']}\n"
    msg += f"📈 Toplam İzlenme: {stats['viewCount']}\n"
    msg += f"🎬 Toplam Video: {stats['videoCount']}\n\n"
    msg += f"💬 *Son Yorumlar:*\n"
    
    for item in comments['items']:
        text = item['snippet']['topLevelComment']['snippet']['textDisplay'][:50]
        author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        msg += f"- {author}: {text}...\n"
        
    return msg

if __name__ == "__main__":
    try:
        report = get_channel_report()
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                      data={"chat_id": TG_ID, "text": report, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Hata: {e}")
