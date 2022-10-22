import csv
import json
import os
import re
from pathlib import Path
from typing import Union

from fake_useragent import UserAgent
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from geopy.geocoders import Yandex

_this_file = Path(__file__).resolve()

DIR_REPO = _this_file.parent.parent.resolve()
DATA_PATH = (DIR_REPO / "data").resolve()
DIR_SCRIPTS = (DIR_REPO / "scripts").resolve()
DIR_SRC = (DIR_REPO / "src").resolve()


def parse_working_hours(morning: str, afternoon: str) -> list[str]:
    """Reformatting working hours to needed format in the 1st task"""
    morning_start = morning.split()[1].strip().replace(".", ":")
    morning_finish = morning.split()[3].strip().replace(".", ":")
    if "Continuado" in afternoon:
        afternoon_start = afternoon.split()[1].strip().replace(".", ":")
        afternoon_finish = afternoon.split()[3].strip().replace(".", ":")
        result = [
            f"mon-thu {morning_start} - {morning_finish}",
            f"fri {afternoon_start} - {afternoon_finish}",
        ]
        return result
    elif "Tarde" in morning:
        afternoon_start = morning.split()[6].strip().replace(".", ":")
        afternoon_finish = morning.split()[8].strip().replace(".", ":")
        afternoon_finish_friday = afternoon.split()[3].strip().replace(".", ":")
        working_hours1 = f"mon-thu {morning_start} - {morning_finish} {afternoon_start}-{afternoon_finish}"
        working_hours2 = f"fri {morning_start} - {morning_finish} {afternoon_start}-{afternoon_finish_friday}"
        result = [working_hours1, working_hours2]
        if "Sábado" in afternoon:
            afternoon_finish_friday = afternoon.split()[4].strip().replace(".", ":")
            result[
                1
            ] = f"fri {morning_start} - {morning_finish} {afternoon_start}-{afternoon_finish_friday}"
            sat_start = afternoon.split()[6].strip().replace(".", ":")
            sat_finish = afternoon.split()[8].strip().replace(".", ":")
            string = f"sat {sat_start} - {sat_finish}"
            result.append(string)
        return result
    else:
        afternoon_start = afternoon.split()[1].strip().replace(".", ":")
        afternoon_finish = afternoon.split()[3].strip().replace(".", ":")
        afternoon_finish_friday = afternoon.split()[10].strip().replace(".", ":")
        working_hours1 = f"mon-thu {morning_start} - {morning_finish} {afternoon_start}-{afternoon_finish}"
        working_hours2 = f"fri {morning_start} - {morning_finish} {afternoon_start}-{afternoon_finish_friday}"
        result = [working_hours1, working_hours2]
        return result


async def get_cords(address: str, api_key: str = None) -> Union[list[float], None]:
    """Function for geocoding. Without any API-key it uses OSM geocoder,
    but it doesn't handle all addresses. With API-key (Yandex for example)
    you can get all cords"""
    if api_key:
        async with Yandex(
            api_key=api_key,
            user_agent=UserAgent().random,
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            location = await geolocator.geocode(address)
            lat, lon = location.latitude, location.longitude
            return [lat, lon]

    else:
        try:
            geolocator = Nominatim(user_agent=UserAgent().random)
            location = geolocator.geocode(address)
            lat, lon = location.latitude, location.longitude
            print(f"OSM cords got - {address}")
            return [lat, lon]
        except AttributeError:
            return None


def get_nums(nums: str) -> list[str]:
    """Getting correct phone numbers from provided string"""
    items_for_replace = ["(", ")", "-", " "]
    for item in items_for_replace:
        nums = nums.replace(item, "")
    result = re.findall(r"\d{5,}", nums)
    return result


def write_data_to_json(data: list[dict], output: str) -> None:
    """Writing data to JSON file"""
    path = os.path.join(DATA_PATH, output)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Finished. The data is written to {path}")


def write_data_to_csv(data: list[dict], output: str) -> None:
    """Writing data to csv file"""
    path = os.path.join(DATA_PATH, output)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())
    print(f"Finished. The data is written to {path}")
