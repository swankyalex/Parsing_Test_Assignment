from typing import Any

import requests
from fake_useragent import UserAgent
from tqdm import tqdm

from utils import get_cords
from utils import get_nums
from utils import write_data_to_json


def get_response(url: str, headers: dict[str, Any], params: dict[str, str]):
    response = requests.post(url=url, headers=headers, data=params).json()
    return response


def parse_data(response):
    result_json = []
    for row in tqdm(response["original"]):
        address = f'{row["city"]}, {row["address"]}'.replace("&quot;", "'")
        latlon = get_cords(address)
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
            "working_hours": hours,
        }
        result_json.append(result)
    return result_json


def main() -> None:
    url = "https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php"
    headers = {
        "user-agent": UserAgent().random,
        "X-Requested-With": "XMLHttpRequest",
    }
    params = {"type": "all"}
    response = get_response(url, headers, params)
    data = parse_data(response)
    write_data_to_json(data, "task3.json")


if __name__ == "__main__":
    main()
