import time
import pprint
from libs.scraping import exec_single_week, exec_single_product
from libs.spreadsheet import SpreadSheetAccessor


ACCESS_SPAN_SEC = 10  # 秒
BASE_URL = "https://www.sej.co.jp"


def fetch_product_list():
    product_list = []
    for week_str in ["thisweek", "nextweek"]:
        url = f"{BASE_URL}/products/a/{week_str}/area/kanto/1/l100/"
        product_list_tmp = exec_single_week(url)
        product_list.extend(product_list_tmp)
        time.sleep(ACCESS_SPAN_SEC)
    return product_list


def fetch_product_detail_list(product_list: list):
    product_detail_list = []
    for product in product_list:
        product_detail = exec_single_product(BASE_URL + product["url"])
        product.update(product_detail)
        product_detail_list.append(product.copy())
        pprint.pprint(product_detail)
        time.sleep(ACCESS_SPAN_SEC)
    return product_detail_list


def main():
    ssaccessor = SpreadSheetAccessor()
    sheet_matrix = ssaccessor.fetch_all_records()
    product_id_set = {row[0] for row in sheet_matrix}
    
    product_list = fetch_product_list()
    
    for product in product_list:
        if product.id in product_id_set:
            continue
        product_detail = exec_single_product(product)
        ssaccessor.append_product_detail(product_detail)
        time.sleep(ACCESS_SPAN_SEC)


if __name__ == "__main__":
    main()
