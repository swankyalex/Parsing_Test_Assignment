import asyncio
import os

import click
import requests
from fake_useragent import UserAgent

from utils import get_cords
from utils import get_nums
from utils import write_data_to_csv
from utils import write_data_to_json


class Parser:
    def __init__(self, link, api_key=None):
        self.rows = None
        self.api_key = api_key
        self.url = link
        self.headers = {
            "user-agent": UserAgent().random,
            "X-Requested-With": "XMLHttpRequest",
        }
        self.data = {"type": "all"}
        self.json = []

    def get_rows(self):
        response = requests.post(
            url=self.url, headers=self.headers, data=self.data
        ).json()
        self.rows = [row for row in response["original"]]

    async def parse_data(self, row):
        """Parse data from JSON"""
        address = f'{row["city"]}, {row["address"]}'.replace("&quot;", "'")
        # if u have YMaps APIkey, you can put it in the function below to get all cords

        latlon = await get_cords(address, self.api_key)
        name = "Natura Siberica"
        phone = row["phone"]
        if phone:
            phones = get_nums(phone)
        else:
            phones = "None"
        hours = row["schedule"]
        result = {
            "address": address,
            "latlon": latlon,
            "name": name,
            "phones": phones,
            "working_hours": [hours],
        }
        self.json.append(result)

    def runner(self):
        print(f"Start parsing data from {self.url}")
        self.get_rows()
        if not self.api_key:
            print("Using OSM geocoder (without api key). Speed - 1 request/sec only")
        tasks = [self.parse_data(row) for row in self.rows]
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(asyncio.wait(tasks))
        return self.json


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
    url = "https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php"
    api_key = None  # you can provide your YM api key here
    parser = Parser(url, api_key)
    data = parser.runner()
    if output == "csv":
        write_data_to_csv(data, "task3.csv")
    else:
        write_data_to_json(data, "task3.json")


if __name__ == "__main__":
    main()
