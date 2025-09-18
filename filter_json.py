import os
import json
import re
import argparse
import hashlib
from typing import Any, Dict, List, Union, Annotated
from pprint import pprint

from jsonpath_ng import jsonpath
from jsonpath_ng import parse as jsonparse
from jsonpointer import JsonPointer, JsonPointerException

JsonPathStr = Annotated[str, "A string formatted as a JSONPath expression from jsonpath_ng."]
# Regex pattern to match device names in the format !ND=DeviceName
# Only works with CISCO
REGEX_STR = r'!ND=([\w\-]*)'


def hash_string(s: str, /) -> str:
    """Returns a SHA-256 hash of the input string.
    
    Args:
        s (str): The input string to hash.
        
    Returns:
        str: The SHA-256 hash of the input string in hexadecimal format.
    """
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


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
            if 'ResyncMarker' in line and '"marker_type":"start"' in line:
                markers.append(json.loads(line))
    return markers


def get_device_mappings(markers: list[dict]) -> dict[str, str]:
    """Get a mapping of device names to their new mangled names.
    
    Args:
        markers (list[dict]): A list of dictionaries representing the start markers.
        
    Returns:
        dict[str, str]: A dictionary mapping device names to their mangled names.
    """
    device_pointer = JsonPointer('/event/marker_scope/filterParam/properties/device')
    device_hashes = {}
    counter = 1
    for marker in markers:
        try:
            device = device_pointer.resolve(marker)
            if device not in device_hashes and (match := re.search(REGEX_STR, device)):
                device_name = match.group(1)
                device_hashes[device_name] = f'DEVICE-{counter:03}'
                counter += 1
        except JsonPointerException as e:
            print(f"Error resolving JSON Pointer: {e}")
    return device_hashes


def mangle_device_names(data: list[dict], device_mappings: dict[str, str]) -> list[dict]:
    """Mangle device names in the data using the provided device hashes.
    
    Args:
        data (list[dict]): A list of dictionaries representing the JSONL data.
        device_hashes (dict[str, str]): A dictionary mapping device names to their SHA-256 hashes.
        
    Returns:
        list[dict]: The modified list of dictionaries with mangled device names.
    """
    device_pattern = re.compile(REGEX_STR)
    
    for entry in data:
        entry_str = json.dumps(entry)
        matches = device_pattern.findall(entry_str)
        for match in matches:
            if match in device_mappings:
                mangled_name = device_mappings[match]
                entry_str = entry_str.replace(f'!ND={match}', f'!ND={mangled_name}')
        entry.update(json.loads(entry_str))
    return data


def nullify_fields(data: list[dict], pointers: list[JsonPathStr]) -> list[dict]:
    """Nullify fields in the data based on the provided JSON Pointers.
    
    Args:
        data (list[dict]): A list of dictionaries representing the JSONL data.
        pointers (list[JsonPointer | str]): A list of JSON Pointers or strings representing the fields to nullify.
        
    Returns:
        list[dict]: The modified list of dictionaries with specified fields set to an empty string.
    """
    result = []
    root_pointer = '$..object_data'
    for pointer in pointers:
        jsonpath_expr = jsonparse(f'{root_pointer}..{pointer}')
        for entry in data:
            result.append(jsonpath_expr.update(entry, ""))
    return result


if __name__ == '__main__':

    with open ('data.jsonl', 'r') as f:
        data = [json.loads(line) for line in f]

    pointers = [
        'userLabel',
        'description',
        'networkConstruct..id'
    ]

    markers = read_start_markers('data.jsonl')
    device_mappings = get_device_mappings(markers)

    mangled_data = mangle_device_names(data, device_mappings)
    mangled_data = nullify_fields(mangled_data, pointers)

    with open('mangled_data.jsonl', 'w') as f:
        for entry in mangled_data:
            f.write(json.dumps(entry).replace(' ', '') + '\n')
    
    for pointer in pointers:
        json_str = f'$..object_data..{pointer}'
        json_expr = jsonparse(json_str)
        print(f'{json_str}: ', [match.value for match in json_expr.find(mangled_data)])

    