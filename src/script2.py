import asyncio
import re
from typing import Any

import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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


async def get_all_links(idx, all_links, url, headers):
    """Getting all links of the shops"""

    params = {"CITY_ID": idx}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, params=params) as resp:
            soup = BeautifulSoup(await resp.text(), "lxml")
            res = soup.find_all("a", class_="btn btn-blue")
            for item in res:
                all_links.append("https://www.som1.ru" + item["href"])


async def parse_data(
    link: list[str], headers: dict[str, Any], result_json
) -> list[dict]:
    """Getting all needed data from provided links"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url=link, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), "lxml")
            description = soup.find("table", class_="shop-info-table").find_all("tr")
            results = [item.find_all("td")[-1].text for item in description]
            address, tel, hours = [*results]
            tel = get_nums(tel)
            name = soup.select(".page-body > div:nth-child(1) > h1:nth-child(1)")[
                0
            ].text
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


def main() -> None:
    url = "https://www.som1.ru/shops/"
    headers = {"user-agent": UserAgent().random}
    all_cities = get_cities_id(url, headers)
    all_links = []
    task = [get_all_links(city, all_links, url, headers) for city in all_cities]
    asyncio.run(asyncio.wait(task))
    result_json = []
    task2 = [parse_data(link, headers, result_json) for link in all_links]
    asyncio.run(asyncio.wait(task2))
    write_data_to_json(result_json, "async_task2.json")


if __name__ == "__main__":
    main()
