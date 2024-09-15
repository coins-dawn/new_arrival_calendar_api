import gspread
import base64
import json
import os
import pprint
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from libs.product import ProductDetail


load_dotenv()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class SpreadSheetAccessor:
    def __init__(self) -> None:
        self.worksheet = SpreadSheetAccessor.__init_worksheet()

    @staticmethod
    def __init_worksheet():
        base64_credentials = os.getenv("SPREADSHEET_SECRET_KEY")
        spreadsheet_key = os.getenv("SPREADSHEET_KEY")
        decoded_credentials_json = base64.b64decode(base64_credentials).decode("utf-8")
        credentials_info = json.loads(decoded_credentials_json)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_info, SCOPE
        )
        client = gspread.authorize(credentials)
        return client.open_by_key(spreadsheet_key).sheet1

    def fetch_all_records(self):
        """シートの中身を二次元配列型式で得する。"""
        sheet_matrix = self.worksheet.get_all_values()
        # ヘッダーを除いて返却する
        return sheet_matrix[1:]

    def clear(self):
        """シートの中身をクリアする。ただしヘッダーは残す。"""
        row_count = self.worksheet.row_count
        if row_count > 1:
            self.worksheet.delete_rows(2, row_count)

    def append_rows(self, product_list: list):
        """シートの末尾にレコードを追加する。"""
        self.worksheet.append_rows(product_list)


if __name__ == "__main__":
    ssaccessor = SpreadSheetAccessor()
    pprint.pprint(ssaccessor.fetch_all_records())
    ssaccessor.clear()
