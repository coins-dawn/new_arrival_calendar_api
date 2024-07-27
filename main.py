import requests
import re
import time
import pprint
from bs4 import BeautifulSoup

ACCESS_SPAN_SEC = 10  # 秒


def convert_date_format(text: str) -> str:
    match = re.search(r"(\d{4})年(\d{2})月(\d{2})日", text)
    if match:
        year, month, day = match.groups()
        month = str(int(month))
        day = str(int(day))
        return f"{year}/{month}/{day}"
    else:
        return None


def exec_single_week(url: str):
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
        arrival = convert_date_format(arrival_str)
        product_list.append(
            {
                "name": product_name,
                "price": price,
                "tax_price": tax_price,
                "arrival": arrival,
                "url": product_url,
            }
        )
    return product_list


def exec_single_product(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # find category
    a_list = soup.find_all("a")
    category = None
    for i, a_elem in enumerate(a_list):
        first_str = a_elem.text
        second_str = a_list[i + 1].text
        third_str = a_list[i + 2].text
        if first_str == "トップ" and second_str == "商品のご案内":
            category = third_str
            break

    # find descripttion
    description = soup.find("div", class_="item_text").text.strip()

    return {"category": category, "description": description}


def main():
    product_list = []
    for week_str in ["thisweek", "nextweek"]:
        url = f"https://www.sej.co.jp/products/a/{week_str}/area/kanto/1/l100/"
        product_list_tmp = exec_single_week(url)
        product_list.extend(product_list_tmp)
        time.sleep(10)

    base_url = "https://www.sej.co.jp/"
    product_detail_list = []
    for product in product_list:
        product_detail = exec_single_product(base_url + product["url"])
        product.update(product_detail)
        product_detail_list.append(product.copy())
        pprint.pprint(product)
        time.sleep(10)


if __name__ == "__main__":
    main()
