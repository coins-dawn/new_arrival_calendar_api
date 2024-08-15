import gspread
import base64
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    load_dotenv()
    base64_credentials = os.getenv("SPREADSHEET_SECRET_KEY")
    spreadsheet_key = os.getenv("SPREADSHEET_KEY")
    
    decoded_credentials_json = base64.b64decode(base64_credentials).decode('utf-8')
    credentials_info = json.loads(decoded_credentials_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    client = gspread.authorize(credentials)
    try:
        # sheet_name = datetime.now().strftime('%Y%m%d')
        # spreadsheet = client.open(spreadsheet_key)
        # worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
        worksheet = client.open_by_key(spreadsheet_key).sheet1
        data = worksheet.get_all_values()
        print("スプレッドシートのデータ:")
        print(data)
        new_data = [['新しいデータ1', '新しいデータ2'], ['新しいデータ3', '新しいデータ4']]
        worksheet.append_rows(new_data)
        print("新しいデータが追加されました。")
    except Exception as e:
        print("エラーが発生しました:", e)

if __name__ == "__main__":
    main()