import pytest
import copy


@pytest.fixture
def example_api_response():
    return {
        "version": 1,
        "header": {
            "envelopeId": "887b3ee5-978f-44e7-9261-8bc60914b4e6",
            "roleIds": [],
            "timestamp": "2025-05-20T12:05:56.705542Z",
            "traceId": "08107431-b079-4f0e-91b0-e0c4f1f2d7e7",
            "upstreamId": "1785f76f-1e22-43db-88fa-d124bdb26e78",
        },
        "event": {
            "_type": "bp.v1.ObjectChanged",
            "object_type": "/bpocore/api/v2/resources/put",
            "op": "updated",
            "object_id": "bf129225-1a26-11f0-abdf-1511c0e6270c___MD=CISCO_EPNM!ND=URDELAB080!CTP=name=PLINE-2-2-TX;lr=lr-optical-section",
            "object_data": {
                "discovered": True,
                "orchState": "active",
                "productId": "urn:cyaninc:bp:product:radciscoepnmerf:tpe",
                "label": "MD=CISCO_EPNM!ND=URDELAB080!CTP=name=PLINE-2-2-TX;lr=lr-optical-section",
                "properties": {
                    "device": "MD=CISCO_EPNM!ND=URDELAB080",
                    "structureType": "CTPServerToClient",
                    "data": {
                        "relationships": {
                            "tpeDiscovered": {
                                "data": {
                                    "type": "tpeDiscovered",
                                    "id": "MD=CISCO_EPNM!ND=URDELAB080!CTP=name=PLINE-2-2-TX;lr=lr-optical-section",
                                }
                            },
                            "networkConstruct": {
                                "data": {
                                    "type": "networkConstructs",
                                    "id": "MD=CISCO_EPNM!ND=URDELAB080",
                                }
                            },
                            "equipment": {
                                "data": {
                                    "type": "equipment",
                                    "id": "MD=CISCO_EPNM!ND=URDELAB080!EQ=name=PUNIT-2;partnumber=N/A!PC=PLINE-2-2-TX",
                                }
                            },
                            "owningServerTpe": {
                                "data": {
                                    "id": "MD=CISCO_EPNM!ND=URDELAB080!PTP=name=PLINE-2-2-TX;lr=lr-optical-physical",
                                    "type": "tpes",
                                }
                            },
                        },
                        "attributes": {
                            "additionalAttributes": {
                                "tp.directionality": "com:tp-source"
                            },
                            "displayAlias": "PLINE-2-2-TX",
                            "userLabel": "",
                            "cardType": "PLACE_HOLDER",
                            "nativeName": "PLINE-2-2-TX",
                            "structureType": "CTPServerToClient",
                            "locations": [
                                {
                                    "managementType": "rest",
                                    "neName": "URDELAB080",
                                    "shelf": "1",
                                    "slot": "PUNIT-2",
                                    "port": "2",
                                }
                            ],
                            "layerTerminations": [
                                {
                                    "layerRate": "OS",
                                    "active": True,
                                    "structureType": "exposed lone cp",
                                    "terminationState": "layer termination cannot terminate",
                                    "layerRateQualifier": "OS",
                                }
                            ],
                            "state": "IS",
                            "category": "CHANNEL_TX",
                        },
                        "type": "tpes",
                        "id": "MD=CISCO_EPNM!ND=URDELAB080!CTP=name=PLINE-2-2-TX;lr=lr-optical-section",
                    },
                },
                "autoClean": False,
                "providerResourceId": "MD=CISCO_EPNM!ND=URDELAB080!CTP=name=PLINE-2-2-TX;lr=lr-optical-section",
                "shared": False,
                "resourceTypeId": "tosca.resourceTypes.TPE",
                "resyncId": "9d71dde4-079a-42e3-9eba-b74c1a6111ae",
            },
        },
    }


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


@pytest.fixture
def example_nested_data():
    return [
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceA",
                    "info": "Some info",
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceB",
                    "info": "Other info",
                    "secret-info": "This info should be a null string.",
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceA",
                    "info": "Repeated device",
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceC",
                    "info": "More info",
                    "secret": {
                        "info": "This info should also be a null string."
                    },
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "DeviceD",
                    "info": "Different format",
                    "secret": {
                        "info": "Make sure to nullify this data!",
                        "public": {
                            "info": "This info should remain unchanged."
                        },
                    },
                }
            }
        },
    ]


@pytest.fixture
def example_null_data():
    return [
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceA",
                    "info": "Some info",
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceB",
                    "info": "Other info",
                    "secret-info": "",
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceA",
                    "info": "Repeated device",
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "MD=CISCO_EPNM!ND=DeviceC",
                    "info": "More info",
                    "secret": {
                        "info": ""
                    },
                }
            }
        },
        {
            "event": {
                "object_data": {
                    "device": "DeviceD",
                    "info": "Different format",
                    "secret": {
                        "info": "",
                        "public": {
                            "info": "This info should remain unchanged."
                        },
                    },
                }
            }
        },
    ]


@pytest.fixture
def example_pointers():
    return [
        "secret-info",
        "secret.info"
    ]


def make_response(base, modifier=None):
    """Factory function for genrerating modified copies of a base response.

    Args:
        base (dict): The base response to copy.
        modifier (callable, optional): A function that takes a dict and
            modifies it in place.
    """
    response = copy.deepcopy(base)
    if modifier:
        modifier(response)
    return response
