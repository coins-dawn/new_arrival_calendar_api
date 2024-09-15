import os
import base64
import json
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


class ImageHandler:
    def __init__(self) -> None:
        self.service = ImageHandler.__init_service()
        self.image_dir = os.getenv("IMAGE_DIR")

    @staticmethod
    def __init_service():
        base64_credentials = os.getenv("SPREADSHEET_SECRET_KEY")
        decoded_credentials_json = base64.b64decode(base64_credentials).decode("utf-8")
        credentials_info = json.loads(decoded_credentials_json)
        creds = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
        return build("drive", "v3", credentials=creds)

    def download_and_upload_image(self, image_url: str) -> str:
        # 画像のダウンロード & 圧縮
        response = requests.get(image_url)
        if response.status_code != 200:
            return None
        image = Image.open(BytesIO(response.content))
        compressed_image_path = "compressed_image.jpg"
        image.save(compressed_image_path, format="JPEG", quality=10)

        # 画像のアップロード
        file_metadata = {"name": "image", "parents": [self.image_dir]}
        media = MediaFileUpload(compressed_image_path, mimetype="image/jpeg")
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        file_id = file.get("id")

        # アクセス権の設定
        permission = {"type": "anyone", "role": "reader"}
        # アクセス権限を設定する
        self.service.permissions().create(fileId=file_id, body=permission).execute()

        return file_id

    def remove_image(self, file_id: str) -> None:
        """画像を削除する。"""
        self.service.files().delete(fileId=file_id).execute()
        print(f"delete file: {file_id}")


if __name__ == "__main__":
    image_handler = ImageHandler()
    file_id = "1q0Jw84ntTutaXU5U8FySficf7lsSKhIa"
    image_handler.remove_image(file_id)
