# Project For Matt

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

## Instructions

1. Find all Device Names
    - Find ReSync Markers
      - Look for `Resync` in `_type` field
      - Look for `start` in `marker_type`
      - If Both are found:
        - Device name under `Filter -> Param -> device`
2. For Each Device:
   1. Create Alias name for device
      - Consider using string hashing
   2. Store Alias <-> Name link (somewhere)
      - Does not need to be saved past runtime
      - Only replace device name after `ND=` string
3. Need list of user-configurable JSON pointers
   - Look for pointers that need to be nullified
   - User should be able to choose which properties to nullify
   - User gives pointers (pointers => paths)
4. Output should be `.jsonl` file with device names replaced AND sensative fields nullified
5. Create Runner in GitLab
   - Run linting check for formatting
   - Dev branch should pass runners before getting merged to main
     
## Notes

- Find device names in Resync object, replace names in BOTH Resync object AND Future lines.
- Each Resync start should have **1 device**
- `object_data` contains the contents of the JSON data
- No `object_data` field in `start` or `end` markers

