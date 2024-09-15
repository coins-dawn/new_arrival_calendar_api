import time
import pprint
from libs.scraping import exec_single_week, exec_single_product
from libs.spreadsheet import SpreadSheetAccessor
from libs.image import ImageHandler
from datetime import datetime, timedelta


ACCESS_SPAN_SEC = 10  # 秒


def fetch_product_list():
    product_list = []
    for week_str in ["thisweek", "nextweek"]:
        url = f"https://www.sej.co.jp/products/a/{week_str}/area/kanto/1/l100/"
        product_list_tmp = exec_single_week(url)
        product_list.extend(product_list_tmp)
        time.sleep(ACCESS_SPAN_SEC)
    return product_list


def is_more_than_one_month_ago(date_str: str) -> bool:
    """
    文字列で与えられた日付が、現在時刻よりも1か月以上前かどうかを判定する関数。

    :param date_str: 2024/8/28 の形式の日付文字列
    :return: True なら1か月以上前、False ならそれ以降
    """
    input_date = datetime.strptime(date_str, "%Y/%m/%d")
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    return input_date < one_month_ago


def main():
    ssaccessor = SpreadSheetAccessor()
    image_handler = ImageHandler()
    sheet_matrix = ssaccessor.fetch_all_records()
    ssaccessor.clear()

    # 1ヶ月以上前に発売したものについては削除
    sheet_matrix_filtered = []
    for row in sheet_matrix:
        if is_more_than_one_month_ago(row[6]):
            file_path = row[8]
            if file_path:
                file_id = file_path.split("/")[-1]
                image_handler.remove_image(file_id)
        else:
            sheet_matrix_filtered.append(row)
    product_id_set = {row[0] for row in sheet_matrix_filtered}

    # スクレイピングで商品データを取得
    new_product_list = []
    product_list = fetch_product_list()
    for product in product_list:
        if product.id in product_id_set:
            continue
        product_detail = exec_single_product(product)
        image_url = ""
        if product_detail.image_url != "":
            file_id = image_handler.download_and_upload_image(product_detail.image_url)
            image_url = "https://lh3.googleusercontent.com/d/" + file_id
        new_product_list.append(product_detail.to_list() + [image_url])
        time.sleep(ACCESS_SPAN_SEC)

    ssaccessor.append_rows(sheet_matrix_filtered + new_product_list)


if __name__ == "__main__":
    main()
