import asyncio
import os
import re

import aiohttp
import click
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from utils import get_nums
from utils import write_data_to_csv
from utils import write_data_to_json


class Parser:
    def __init__(self, link):
        self.url = link
        self.headers = {"user-agent": UserAgent().random}
        self.city_idxs = []
        self.all_links = []
        self.data = []

    def get_cities_id(self):
        """Get all cities id from site"""
        response = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")
        soup = soup.find_all("div", class_="cities-container")
        for item in soup:
            result = item.find_all("label")
            for x in result:
                self.city_idxs.append(x["id"])

    async def get_all_links(self, idx):
        """Getting all links of the shops"""
        params = {"CITY_ID": idx}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.url, headers=self.headers, params=params
            ) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
                res = soup.find_all("a", class_="btn btn-blue")
                for item in res:
                    self.all_links.append("https://www.som1.ru" + item["href"])

    async def parse_data(self, link):
        """Getting all needed data from provided links"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url=link, headers=self.headers) as resp:
                soup = BeautifulSoup(await resp.text(), "lxml")
                description = soup.find("table", class_="shop-info-table").find_all(
                    "tr"
                )
                results = [item.find_all("td")[-1].text for item in description]
                address, tel, hours = results
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
                self.data.append(result)

    def runner(self):
        print(f"Start parsing data from {self.url}")
        self.get_cities_id()
        print("City indexes received")
        tasks = [self.get_all_links(idx) for idx in self.city_idxs]
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(asyncio.wait(tasks))
        print("All links received")
        tasks2 = [self.parse_data(link) for link in self.all_links]
        asyncio.run(asyncio.wait(tasks2))
        return self.data


@click.command()
@click.option(
    "-o",
    "--output",
    default="json",
    type=click.Choice(["json", "csv"]),
    help=f"Choose processing type",
    show_default=True,
)
def main(output: str) -> None:
    url = "https://www.som1.ru/shops/"
    parser = Parser(url)
    data = parser.runner()
    write_data_to_json(data, "task2.json") if output == "json" else write_data_to_csv(
        data, "task2.csv"
    )


if __name__ == "__main__":
    main()
