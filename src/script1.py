import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils import parse_working_hours
from utils import write_data_to_json


def get_all_links(url: str) -> list[str]:
    """Getting all shop links on the site"""
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "lxml")
    results = soup.find_all("ul", class_="sub-menu")
    all_links = []
    for result in results:
        all_links.extend(
            ["https://oriencoop.cl" + item["href"] for item in result.find_all("a")]
        )
    return all_links


def parse_data(all_links: list[str]) -> list[dict]:
    """Getting all needed data from provided links"""
    result_json = []
    for link in tqdm(all_links):
        response = requests.get(url=link)
        soup = BeautifulSoup(response.text, "lxml")
        all_items = soup.find_all("div", class_="sucursal")
        for item in all_items:
            address = item.find("div", class_="s-dato").find("span").text
            coord = item.find("div", class_="s-mapa").find("iframe")["src"]
            lat = " ".join(re.findall(r"2d([^<>]+)!", coord)).split("!")[0]
            lon = " ".join(re.findall(r"3d([^<>]+)!", coord)).split("!")[0]
            latlon = [float(lat), float(lon)]
            name = "Oriencoop"
            first_phone = item.select(".s-dato > p:nth-child(3) > span:nth-child(3)")[
                0
            ].text.replace("-", "")
            second_phone = soup.select(".b-call > a:nth-child(3)")[0].text
            third_phone = soup.select(".b-call > a:nth-child(6)")[0].text.replace(
                " ", ""
            )
            phones = [first_phone, second_phone, third_phone]
            morning = item.select(".s-dato > p:nth-child(5) > span:nth-child(3)")[
                0
            ].text
            afternoon = item.select(".s-dato > p:nth-child(5) > span:nth-child(5)")[
                0
            ].text
            working_hours = parse_working_hours(morning, afternoon)
            result = {
                "address": address,
                "latlon": latlon,
                "name": name,
                "phones": phones,
                "working_hours": working_hours,
            }
            result_json.append(result)
    return result_json


def main() -> None:
    url = "https://oriencoop.cl/sucursales.htm"
    all_links = get_all_links(url)
    data = parse_data(all_links)
    write_data_to_json(data, "task1.json")


if __name__ == "__main__":
    main()
