import requests
import json
import os
import time
from datetime import datetime, timedelta, timezone

CLIENT_ID = 'your twitch client id'
CLIENT_SECRET = 'your twitch client secret'
CHANNEL_NAME = 'polling target channel name'
DISCORD_WEBHOOK_URL = 'your discord webhook url'

STATE_FILE = 'sent_clips.json' # Discordに送信済みのclipIDを保存するファイル
MAX_CLIPS = 100  # 1回あたり取得・投稿する最大件数
POST_INTERVAL = 1.5  # Discord送信間隔（秒）

def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return resp.json()['access_token']

def get_user_id(username, access_token):
    url = 'https://api.twitch.tv/helix/users'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    params = {'login': username}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data['data']:
        return data['data'][0]['id']
    return None

def get_latest_clips(user_id, access_token, count=MAX_CLIPS):
    # 期間を設定
    now_utc = datetime.now(timezone.utc)
    one_month_ago = now_utc - timedelta(days=7)

    # RFC3339 形式に変換
    started_at = one_month_ago.isoformat(timespec='seconds').replace('+00:00', 'Z')
    ended_at = now_utc.isoformat(timespec='seconds').replace('+00:00', 'Z')

    url = 'https://api.twitch.tv/helix/clips'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'broadcaster_id': user_id
        ,'first': count
        ,'started_at': started_at
        ,"ended_at": ended_at
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get('data', [])

def load_sent_clip_ids():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, 'r') as f:
        return set(json.load(f))

def save_sent_clip_ids(clip_ids):
    with open(STATE_FILE, 'w') as f:
        json.dump(list(clip_ids), f)

def send_discord_message(message):
    resp = requests.post(DISCORD_WEBHOOK_URL, json={'content': message})
    resp.raise_for_status()

def main():
    access_token = get_access_token()
    user_id = get_user_id(CHANNEL_NAME, access_token)
    if not user_id:
        print("ユーザーIDが見つかりませんでした")
        return

    clips = get_latest_clips(user_id, access_token, count=MAX_CLIPS)

    sent_ids = load_sent_clip_ids()
    new_clips = [clip for clip in clips if clip['id'] not in sent_ids]

    if not new_clips:
        print("新しいクリップはありません")
        return

    # 最新順にソート（作成日時降順）
    new_clips.sort(key=lambda x: x['created_at'], reverse=True)

    # 古い順に送信（Discordは送った順に並ぶため）
    for clip in reversed(new_clips):
        message = (
            f"🎬 クリップ: **{clip['title']}**\n"
            f"作成日時: {clip['created_at']}\n"
            f"{clip['url']}"
        )
        send_discord_message(message)
        print(f"Discordに送信: {clip['title']}")
        sent_ids.add(clip['id'])
        time.sleep(POST_INTERVAL)

    save_sent_clip_ids(sent_ids)

if __name__ == '__main__':
    main()
