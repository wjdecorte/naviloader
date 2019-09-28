import random
import string
import json
import os
from typing import List, Dict

from dateutil.relativedelta import relativedelta
from dateutil.utils import today


def create_fake_data():
    return "".join(
        [random.choice(string.ascii_lowercase) for i in range(random.randint(5, 50))]
    )


def create_duplicates(record_list: List[Dict]) -> List[Dict]:
    """
    Duplicate random records (id/ts)
    :param record_list: list of records
    :return: list
    """
    duplicate_count = random.randint(1, len(record_list))
    new_record_list = record_list.copy()
    for i in range(duplicate_count):
        record_id = random.randint(0, len(record_list) - 1)
        new_record = record_list[record_id].copy()
        new_record["data"] = create_fake_data()
        new_record_list.append(new_record)
    return new_record_list


def create_record():
    """ Create a random record """
    ts = (
        today()
        - relativedelta(days=random.randint(1, 30), seconds=random.randint(0, 86400))
    ).isoformat()
    return dict(
        id=str(random.randint(10100, 10200)),
        data=create_fake_data(),
        ts=ts + "." + str(random.randint(111, 999)) + "Z",
    )


def create_file(record_count: int, data_dir: str, filename: str, make_duplicates: bool):
    """
    Create a file with a random sample of data
    :param record_count: Number of records to write to the file
    :param data_dir: Directory to write the file
    :param filename: Name of the file without extension"
    :return:
    """
    ext = ".json"
    with open(os.path.join(data_dir, f"{filename}{ext}"), "w") as outfile:
        record_list = [create_record() for i in range(record_count)]
        if make_duplicates:
            record_list = create_duplicates(record_list)
        json.dump(dict(records=record_list), outfile)
