import pytest
from ..filter_json import mangle_device_names, get_device_mappings
from .utils import make_test_cases


@pytest.fixture
def example_jsonl_data():
    return [
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DeviceA",
                    "info": "Some info",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DeviceB",
                    "info": "Other info",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DeviceA",
                    "info": "Repeated device",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DeviceC",
                    "info": "More info",
                }
            }
        },
        {
            "event": {
                "properties": {"device": "DeviceD", "info": "Different format"}
            }
        },
    ]


@pytest.fixture
def example_device_mappings():
    return {
        "DeviceA": "DEVICE-001",
        "DeviceB": "DEVICE-002",
        "DeviceC": "DEVICE-003",
        "DeviceD": "DEVICE-004",
    }


@pytest.fixture
def example_mangled_data():
    return [
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DEVICE-001",
                    "info": "Some info",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DEVICE-002",
                    "info": "Other info",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DEVICE-001",
                    "info": "Repeated device",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=DEVICE-003",
                    "info": "More info",
                }
            }
        },
        {
            "event": {
                "properties": {
                    "device": "DEVICE-004",
                    "info": "Different format",
                }
            }
        },
    ]


@pytest.fixture
def example_device_pairs():
    return [
        (
            "MD=CISCO_EPNM!ND=UNCERTO030-Lab4206-C",
            "MD=CISCO_EPNM!ND=DEVICE-001",
        ),
        ("MD=CISCO_EPNM!ND=URZELAB077", "MD=CISCO_EPNM!ND=DEVICE-002"),
        ("USMDF-007", "DEVICE-003"),
    ]


def test_get_device_mappings(example_jsonl_data, example_device_mappings):
    """Test the get_device_mappings function."""
    assert get_device_mappings(example_jsonl_data) == example_device_mappings


def test_mangle_device_names(
    example_jsonl_data, example_device_mappings, example_mangled_data
):
    """Test the mangle_device_names function."""
    assert (
        mangle_device_names(example_jsonl_data, example_device_mappings) == example_mangled_data
    )


def test_map_and_mangle(example_jsonl_data, example_mangled_data):
    """Test the combined mapping and mangling process."""
    device_mappings = get_device_mappings(example_jsonl_data)
    mangled_data = mangle_device_names(example_jsonl_data, device_mappings)
    assert mangled_data == example_mangled_data


def test_auto_generate_example(example_device_pairs):
    inputs, expected = make_test_cases(example_device_pairs)
    device_mappings = get_device_mappings(inputs)
    mangled_data = mangle_device_names(inputs, device_mappings)
    assert mangled_data == expected
