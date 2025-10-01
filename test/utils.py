import uuid
import datetime
import json


def make_test_cases(devices):
    """
    Given a list of (device_name, obfuscated_name) tuples,
    returns (input_objects, output_objects).
    """

    inputs = []
    outputs = []

    for i, (device, obf) in enumerate(devices, start=1):
        # Generate some dummy but stable values
        envelope_id = str(uuid.uuid4())
        marker_id = str(uuid.uuid4())
        timestamp = (
            datetime.datetime(2025, 5, 20, 12, 5, 51 + i).isoformat() + "Z"
        )
        reason = f"{100 + i*10} resource(s)"

        base_obj = {
            "version": 1,
            "header": {
                "envelopeId": envelope_id,
                "roleIds": [],
                "timestamp": timestamp,
            },
            "event": {
                "_type": "bp.v2.ResyncMarker",
                "marker_type": "start",
                "marker_id": marker_id,
                "domain_id": "bf129225-1a26-11f0-abdf-1511c0e6270c",
                "is_full": True,
                "marker_scope": {
                    "resourceTypes": [
                        "tosca.resourceTypes.NetworkConstruct",
                        "tosca.resourceTypes.TPE",
                        "tosca.resourceTypes.FRE",
                        "tosca.resourceTypes.Equipment",
                    ],
                    "filterParam": {"properties": {"device": device}},
                    "providerResourceId": "urn:ciena:bp:ra:radciscoepnmerf",
                },
                "reason": reason,
            },
        }

        # Make a copy for obfuscated version
        obf_obj = base_obj.copy()
        obf_obj = {
            **base_obj,
            "event": {
                **base_obj["event"],
                "marker_scope": {
                    **base_obj["event"]["marker_scope"],
                    "filterParam": {"properties": {"device": obf}},
                },
            },
        }

        inputs.append(base_obj)
        outputs.append(obf_obj)

    return inputs, outputs


if __name__ == "__main__":
    devices = [
        (
            "MD=CISCO_EPNM!ND=UNCERTO030-Lab4206-C",
            "MD=CISCO_EPNM!ND=DEVICE-001",
        ),
        ("MD=CISCO_EPNM!ND=URZELAB077", "MD=CISCO_EPNM!ND=DEVICE-002"),
        ("USMDF-007", "DEVICE-003"),
    ]

    inputs, expected = make_test_cases(devices)

    for input, output in zip(inputs, expected):
        print("Input:")
        print(json.dumps(input, indent=2))
        print("Expected Output:")
        print(json.dumps(output, indent=2))
        print()
