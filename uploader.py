import logging
import os
import pickle
import requests
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logging.basicConfig(level=logging.INFO)

class SocialMediaUploader:
    def __init__(self, client_secrets_file, credentials_file, config_file):
        logging.info("Initializing SocialMediaUploader")
        self.client_secrets_file = client_secrets_file
        self.credentials_file = credentials_file
        self.config_file = config_file
        self.youtube = self.get_authenticated_service()
        self.tiktok_access_token = self.load_tiktok_access_token()

    def load_tiktok_access_token(self):
        logging.info(f"Loading TikTok access token from {self.config_file}")
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config.get('tiktok_access_token')
        else:
            logging.error(f"Config file {self.config_file} not found")
            return None

    def get_authenticated_service(self):
        logging.info("Authenticating with YouTube API")
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        creds = None
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, scopes)
                creds = flow.run_local_server(port=0)
            with open(self.credentials_file, 'wb') as token:
                pickle.dump(creds, token)

        return build('youtube', 'v3', credentials=creds)

    def upload_to_youtube(self, file_path, title, description, tags, category_id, privacy_status):
        logging.info(f"Uploading video to YouTube: {file_path}")
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logging.info(f"Uploaded {int(status.progress() * 100)}%")

        logging.info("YouTube upload complete")
        return response

    def upload_to_tiktok(self, file_path, title):
        logging.info(f"Uploading video to TikTok: {file_path}")
        try:
            tiktok_api_url = "https://api.tiktok.com/upload"
            access_token = self.tiktok_access_token

            if not access_token:
                logging.error("TikTok access token not found")
                return None

            # Prepare the request payload
            files = {'video': open(file_path, 'rb')}
            data = {'title': title, 'access_token': access_token}

            # Send the request to TikTok API
            response = requests.post(tiktok_api_url, files=files, data=data)

            if response.status_code == 200:
                logging.info("TikTok upload complete")
                return response.json()
            else:
                logging.error(f"Failed to upload video to TikTok: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logging.error(f"Exception occurred while uploading to TikTok: {e}")
            return None

    def upload_to_instagram(self, file_path, title):
        logging.info(f"Uploading video to Instagram: {file_path}")
        # Placeholder for Instagram upload logic
        logging.info("Instagram upload complete")

if __name__ == "__main__":
    uploader = SocialMediaUploader("client_secrets.json", "youtube_credentials.pickle", "config.json")
    response = uploader.upload_to_youtube(
        file_path="video.mp4",
        title="Sample Video",
        description="This is a sample video upload.",
        tags=["sample", "video", "upload"],
        category_id="22",  # Category ID for People & Blogs
        privacy_status="public"
    )
    logging.info(f"YouTube video uploaded: {response}")

    uploader.upload_to_tiktok("video.mp4", "Sample Video")
    uploader.upload_to_instagram("video.mp4", "Sample Video")
