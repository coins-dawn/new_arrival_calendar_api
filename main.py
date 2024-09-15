import time
import pprint
from libs.scraping import exec_single_week, exec_single_product
from libs.spreadsheet import SpreadSheetAccessor
from libs.image import ImageUploader


ACCESS_SPAN_SEC = 10  # 秒


def fetch_product_list():
    product_list = []
    for week_str in ["thisweek", "nextweek"]:
        url = f"https://www.sej.co.jp/products/a/{week_str}/area/kanto/1/l100/"
        product_list_tmp = exec_single_week(url)
        product_list.extend(product_list_tmp)
        time.sleep(ACCESS_SPAN_SEC)
    return product_list


def main():
    ssaccessor = SpreadSheetAccessor()
    image_uploader = ImageUploader()
    sheet_matrix = ssaccessor.fetch_all_records()
    product_id_set = {row[0] for row in sheet_matrix}

    product_list = fetch_product_list()

    for product in product_list:
        if product.id in product_id_set:
            continue
        product_detail = exec_single_product(product)
        image_url = ""
        if product_detail.image_url != "":
            file_id = image_uploader.download_and_upload_image(product_detail.image_url)
            image_url = "https://lh3.googleusercontent.com/d/" + file_id
        ssaccessor.append_product_detail(product_detail, image_url)
        time.sleep(ACCESS_SPAN_SEC)


if __name__ == "__main__":
    main()
