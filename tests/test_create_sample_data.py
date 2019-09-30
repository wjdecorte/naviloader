""" Test the create sample data functions """
import tempfile
import os
import json

from navis_loader.create_sample_data import (
    create_file,
    create_record,
    create_fake_data,
    create_duplicates,
)


def test_create_fake_data():
    """ Test fake data creation """
    data = create_fake_data()
    assert data is not None
    assert 4 < len(data) < 51


def test_create_duplicates():
    """ Test duplication of records """

    def getuid(record: dict) -> tuple:
        return record["id"], record["ts"]

    record_list = [create_record(), create_record()]
    dupe_list = create_duplicates(record_list)
    assert len(dupe_list) > len(record_list)
    assert (getuid(dupe_list[0]) == getuid(dupe_list[2])) or (
        getuid(dupe_list[1]) == getuid(dupe_list[2])
    )


def test_create_record():
    """ test creating a sample record """
    record = create_record()
    assert isinstance(record, dict)
    assert "id" in record
    assert "data" in record
    assert "ts" in record


def test_create_file():
    """ test creating a sample file """
    record_count = 5
    filename = "sample_file"
    with tempfile.TemporaryDirectory() as data_dir:
        create_file(record_count, data_dir, filename, make_duplicates=False)
        sample_file_name = os.path.join(data_dir, filename + ".json")
        assert os.path.isfile(sample_file_name)
        sample_file = open(sample_file_name, "r")
        # test the file can be successfully read
        records = json.load(sample_file)
