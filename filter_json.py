import json
import re
from argparse import ArgumentParser
import hashlib
from typing import Annotated

from jsonpath_ng import parse as jsonparse

JsonPathStr = Annotated[
    str, "A string formatted as a JSONPath expression from jsonpath_ng."
]
# Regex pattern to match device names in the format !ND=DeviceName
# Only works with CISCO
REGEX_STR = r"!ND=([\w\-]*)"
DEVICE_PATTERN_ND = re.compile(r"!ND=([\w\-]+)")
DEVICE_PATTERN_PLAIN = re.compile(r"^[\w\-]+$")


def hash_string(s: str, /) -> str:
    """Returns a SHA-256 hash of the input string.

    Args:
        s (str): The input string to hash.

    Returns:
        str: The SHA-256 hash of the input string in hexadecimal format.
    """
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def read_device_mappings(file: str) -> dict[str, str]:
    """Read device mappings from a JSON file.

    Args:
        file (str): The path to the JSON file containing device mappings.

    Returns:
        dict[str, str]: A dictionary mapping device names
                        to their mangled names.
    """
    # Get Resync Start markers using jsonparse
    markers = []
    with open(file) as f:
        for line in f:
            if "ResyncMarker" in line:
                entry = json.loads(line)
                json_marker_type = jsonparse("$.event.marker_type")
                if (
                    match := json_marker_type.find(entry)[0]
                ) and match.value == "start":
                    markers.append(entry)

    # Extract device mappings from markers
    return get_device_mappings(markers)


def read_start_markers(file: str) -> list[dict]:
    """Get the Start markers from a JSONL file.

    Args:
        file (str): The path to the JSONL file.

    Returns:
        list[dict]: A list of dictionaries representing the start markers.
    """
    markers = []
    with open(file) as f:
        for line in f:
            if "ResyncMarker" in line and '"marker_type":"start"' in line:
                markers.append(json.loads(line))
    return markers


def get_device_mappings(markers: list[dict]) -> dict[str, str]:
    """Get a mapping of device names to their new mangled names.

    Args:
        markers (list[dict]): A list of dictionaries representing
                              the start markers.

    Returns:
        dict[str, str]: A dictionary mapping device names
                        to their mangled names.
    """
    jsonpath_expr = jsonparse("$..properties.device")
    mappings = {}
    counter = 1
    for marker in markers:
        matches = jsonpath_expr.find(marker)
        for match in matches:
            # Extract device names using regex
            device = match.value
            if nd_name := DEVICE_PATTERN_ND.search(device):
                device_name = nd_name.group(1)
            else:
                device_name = device
            # Add extracted names to mappings if not present
            if device_name not in mappings:
                mappings[device_name] = f"DEVICE-{counter:03}"
                counter += 1
    return mappings


def mangle_device_names(
    data: list[dict], device_mappings: dict[str, str]
) -> list[dict]:
    """Mangle device names in the data using the provided device hashes.

    Args:
        data (list[dict]): A list of dictionaries representing the JSONL data.
        device_mappings (dict[str, str]): A dictionary mapping device names
                                          to their mangled names.

    Returns:
        list[dict]: The list of dictionaries with mangled device names.
    """
    new_data = data.copy()
    for entry in new_data:
        entry_str = json.dumps(entry)
        for device, mangled_name in device_mappings.items():
            entry_str = entry_str.replace(f"{device}", f"{mangled_name}")
        entry.update(json.loads(entry_str))

    return new_data


def nullify_fields(
    data: list[dict], pointers: list[JsonPathStr]
) -> list[dict]:
    """Nullify fields in the data based on the provided JSON Pointers.

    Args:
        data (list[dict]): A list of dictionaries representing the JSONL data.
        pointers (list[JsonPathStr]): A list of JSON Pointers or strings
                                      representing the fields to nullify.

    Returns:
        list[dict]: The modified list of dictionaries with specified fields
                    set to an empty string.
    """
    if not pointers:
        return data
    result = []
    root_pointer = "$..object_data"
    for pointer in pointers:
        jsonpath_expr = jsonparse(f"{root_pointer}..{pointer}")
        for entry in data:
            result.append(jsonpath_expr.update(entry, ""))
    return result


def mangle_json_file(
    input_file: str, output_file: str, pointers: list[JsonPathStr]
) -> None:
    """Mangle device names and nullify specified fields in a JSONL file.

    Writes the modified data to a new JSONL file.

    Args:
        input_file (str): The path to the input JSONL file.
        output_file (str): The path to the output JSONL file.
        pointers (list[JsonPathStr]): A list of JSON Pointers or strings
                                    representing the fields to nullify.
    """
    # Get the devide name mapping from Resync start markers
    markers = read_start_markers(input_file)
    device_mappings = get_device_mappings(markers)

    # Read the input JSONL file
    with open(input_file, "r") as f:
        data = [json.loads(line) for line in f]

    # Mangle device names and nullify specified fields
    mangled_data = mangle_device_names(data, device_mappings)
    mangled_data = nullify_fields(mangled_data, pointers)

    # Write the modified data to the output JSONL file
    with open(output_file, "w") as f:
        for entry in mangled_data:
            f.write(json.dumps(entry).replace(" ", "") + "\n")


if __name__ == "__main__":
    parser = ArgumentParser(description="Filter and mangle JSONL data.")
    parser.add_argument(
        "--input", "-i", type=str, required=True, help="Input JSONL file path."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        default="mangled_data.jsonl",
        help="Output JSONL file path.",
    )
    parser.add_argument(
        "--pointers",
        "-p",
        type=str,
        nargs="+",
        required=False,
        default=[],
        help="List of JSON Pointers to nullify.",
    )
    parser.add_argument(
        "--pointer_file",
        "-f",
        type=str,
        required=False,
        help="File containing JSON Pointers to nullify, one per line.",
    )

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    # Get pointers from command line list and specified file
    pointers = args.pointers
    if args.pointer_file:
        with open(args.pointer_file, "r") as pf:
            pointers.extend([line.strip() for line in pf if line.strip()])

    mangle_json_file(input_file, output_file, pointers)

    print(f"Mangled data written to {output_file}")
