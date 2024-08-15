import requests
import re
import pprint
from bs4 import BeautifulSoup
from libs.product import Product, ProductDetail


BASE_URL = "https://www.sej.co.jp"


def _convert_date_format(text: str) -> str:
    """日付のフォーマットを変換する"""
    match = re.search(r"(\d{4})年(\d{2})月(\d{2})日", text)
    if match:
        year, month, day = match.groups()
        month = str(int(month))
        day = str(int(day))
        return f"{year}/{month}/{day}"
    else:
        return None


def exec_single_week(url: str):
    """スクレイピングで1週間の新商品を取得する。"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    div_list_inner_list = soup.find_all("div", class_="list_inner")
    product_list = []
    for div_list_inner in div_list_inner_list:
        product_name = div_list_inner.find("div", class_="item_ttl").text.replace(
            "\u3000", ""
        )
        product_url = div_list_inner.find("a").get("href")
        price_str = div_list_inner.find("div", class_="item_price").text
        price = price_str.split("円")[0]
        tax_price = price_str.split("税込")[1].split("円")[0]
        arrival_str = div_list_inner.find("div", class_="item_launch").text
        arrival = _convert_date_format(arrival_str)
        product_id = product_url.split("/")[4]
        product_list.append(
            Product(
                id=product_id,
                name=product_name,
                price=price,
                tax_price=tax_price,
                arrival=arrival,
                url=BASE_URL + product_url
            )
        )
    return product_list


def exec_single_product(product: Product):
    """スクレイピングで1商品の詳細情報を取得する。"""
    response = requests.get(product.url)
    soup = BeautifulSoup(response.content, "html.parser")

    # find category
    a_list = soup.find_all("a")
    category = ""
    for i, a_elem in enumerate(a_list):
        if i >= len(a_list) - 3:
            break
        first_str = a_elem.text
        second_str = a_list[i + 1].text
        third_str = a_list[i + 2].text
        if first_str == "トップ" and second_str == "商品のご案内":
            if "/products/a/" in a_list[i + 2].get("href"):
                category = third_str
                break

    # find descripttion
    description = ""
    description_list = soup.find_all("div", class_="item_text")
    if len(description_list) != 0:
        description = description_list[0].text.strip()
        
    # image url
    image_url = ""
    product_wrap_list = soup.find_all("div", class_="productWrap")
    if len(product_wrap_list) != 0:
        image_url = product_wrap_list[0].find("img")["src"]
    

    return ProductDetail(
        product=product,
        category=category,
        description=description,
        image_url=image_url
    )
