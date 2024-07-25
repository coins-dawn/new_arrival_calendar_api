import requests
import re
import time
import pprint
from bs4 import BeautifulSoup

ACCESS_SPAN_SEC = 10 # 秒


def convert_date_format(text: str) -> str:
    match = re.search(r'(\d{4})年(\d{2})月(\d{2})日', text)
    if match:
        year, month, day = match.groups()
        month = str(int(month))
        day = str(int(day))
        return f"{year}/{month}/{day}"
    else:
        return None


def exec_single_week(url: str):
    response = requests.get(url)
    time.sleep(10)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_list_inner_list = soup.find_all("div", class_="list_inner")
    response_list = []
    for div_list_inner in div_list_inner_list:
        product_name = div_list_inner.find("div", class_="item_ttl").text.replace("\u3000", "")
        product_url = div_list_inner.find("a").get("href")
        price_str = div_list_inner.find("div", class_="item_price").text
        price = price_str.split("円")[0]
        tax_price = price_str.split("税込")[1].split("円")[0]
        arrival_str = div_list_inner.find("div", class_="item_launch").text
        arrival = convert_date_format(arrival_str)
        response_list.append(
            {
                "name": product_name,
                "price": price,
                "tax_price": tax_price,
                "arrival": arrival,
                "url": product_url
            }    
        )
    return response_list


def main():
    for week_str in ["thisweek", "nextweek"]:
        url = f"https://www.sej.co.jp/products/a/{week_str}/area/kanto/1/l100/"
        response_list = exec_single_week(url)
        for response in response_list:
            pprint.pprint(response)


if __name__ == "__main__":
    main()
