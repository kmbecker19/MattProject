from ..filter_json import mangle_device_names, get_device_mappings, nullify_fields
from .utils import make_test_cases


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
    input_data, expected_data = make_test_cases(example_device_pairs)
    device_mappings = get_device_mappings(input_data)
    mangled_data = mangle_device_names(input_data, device_mappings)
    assert mangled_data == expected_data


def test_nullify_fields(example_nested_data, example_null_data, example_pointers):
    output_data = nullify_fields(example_nested_data, example_pointers)
    assert output_data == example_null_data
