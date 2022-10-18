import re
from typing import Any

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm

from utils import get_nums
from utils import write_data_to_json


def get_cities_id(url: str, headers: dict[str, Any]) -> list[str]:
    """Get all cities id from site"""
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    soup = soup.find_all("div", class_="cities-container")
    all_cities = []
    for item in soup:
        result = item.find_all("label")
        for x in result:
            all_cities.append(x["id"])
    return all_cities


def get_all_links(
    all_cities: list[str], url: str, headers: dict[str, Any]
) -> list[str]:
    """Getting all links of the shops"""
    all_links = []
    for city in tqdm(all_cities):
        params = {"CITY_ID": city}
        response = requests.post(url=url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, "lxml")
        res = soup.find_all("a", class_="btn btn-blue")
        for item in res:
            all_links.append("https://www.som1.ru" + item["href"])
    return all_links


def parse_data(all_links: list[str], headers: dict[str, Any]) -> list[dict]:
    """Getting all needed data from provided links"""
    result_json = []
    for link in tqdm(all_links):
        response = requests.get(url=link, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        description = soup.find("table", class_="shop-info-table").find_all("tr")
        results = [item.find_all("td")[-1].text for item in description]
        address, tel, hours = [*results]
        tel = get_nums(tel)
        name = soup.select(".page-body > div:nth-child(1) > h1:nth-child(1)")[0].text
        cords = soup.select("body > script:nth-child(82)")[0].text
        result = re.findall(r"[\d]+[.,\d]+", cords)
        cords = [float(item) for item in result]
        result = {
            "address": address,
            "latlon": cords,
            "name": name,
            "phones": tel,
            "working_hours": hours,
        }
        result_json.append(result)
    return result_json


def main() -> None:
    url = "https://www.som1.ru/shops/"
    headers = {"user-agent": UserAgent().random}
    all_cities = get_cities_id(url, headers)
    all_links = get_all_links(all_cities, url, headers)
    data = parse_data(all_links, headers)
    write_data_to_json(data, "task2.json")


if __name__ == "__main__":
    main()
