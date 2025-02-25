from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

logging.basicConfig(level=logging.INFO)

class YouTubeUploader:
    def __init__(self, client_secrets_file, credentials_file):
        logging.info("Initializing YouTubeUploader")
        self.client_secrets_file = client_secrets_file
        self.credentials_file = credentials_file
        self.youtube = self.get_authenticated_service()

    def get_authenticated_service(self):
        logging.info("Authenticating with YouTube API")
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import os
        import pickle

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

    def upload_video(self, file_path, title, description, tags, category_id, privacy_status):
        logging.info(f"Uploading video: {file_path}")
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

        logging.info("Upload complete")
        return response

if __name__ == "__main__":
    uploader = YouTubeUploader("client_secrets.json", "youtube_credentials.pickle")
    response = uploader.upload_video(
        file_path="video.mp4",
        title="Sample Video",
        description="This is a sample video upload.",
        tags=["sample", "video", "upload"],
        category_id="22",  # Category ID for People & Blogs
        privacy_status="public"
    )
    logging.info(f"Video uploaded: {response}")
