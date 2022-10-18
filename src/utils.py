import json
import os
import re

from fake_useragent import UserAgent
from geopy.geocoders import Nominatim
from geopy.geocoders import Yandex


def parse_working_hours(morning, afternoon):
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


def get_cords(address, api_key=None):
    try:
        if api_key:
            geolocator = Yandex(api_key=api_key, user_agent=UserAgent().random)
        else:
            geolocator = Nominatim(user_agent=UserAgent().random)
        location = geolocator.geocode(address)
        lat, lon = location.latitude, location.longitude
        return [lat, lon]
    except:
        return None


def get_nums(nums):
    items_for_replace = ["(", ")", "-", " "]
    for item in items_for_replace:
        nums = nums.replace(item, "")
    result = re.findall(r"\d{5,}", nums)
    return result


def write_data_to_json(result, output):
    path = os.path.join("../data/", output)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    print(f"data written to {path}")
