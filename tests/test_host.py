# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

from copy import deepcopy

import pytest
from jsonschema import ValidationError

from mirrormanager_messages.host import (
    HostAddedV1,
    HostAddedV2,
    HostCrawlerDisabledV1,
    HostDeletedV1,
    HostDeletedV2,
    HostUpdatedV1,
    HostUpdatedV2,
)

from .utils import DUMMY_HOST, DUMMY_SITE


def test_minimal_added():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {"agent": "dummy-user", "host": DUMMY_HOST, "site": DUMMY_SITE}
    message = HostAddedV2(body=body)
    message.validate()
    assert message.url is None
    assert message.agent_name == "dummy-user"
    assert message.usernames == ["dummy-admin", "dummy-user"]
    assert message.agent_avatar == (
        "https://seccdn.libravatar.org/avatar/"
        "18e8268125372e35f95ef082fd124e9274d46916efe2277417fa5fecfee31af1"
        "?s=64&d=retro"
    )
    assert message.summary == "Host dummy-host has been added to site dummy-site by dummy-user"
    assert str(message) == "Host name: dummy-host\nCountry: US\nBandwitdh: 1\nSite: dummy-site\n"


def test_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {
        "agent": "dummy-user",
        "host": {"id": 1},
    }
    message = HostAddedV2(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_updated():
    body = {"agent": "dummy-user", "host": DUMMY_HOST, "site": DUMMY_SITE}
    message = HostUpdatedV2(body=body)
    message.validate()
    assert message.summary == "Host dummy-host in site dummy-site has been updated by dummy-user"
    assert str(message) == "Host name: dummy-host\nCountry: US\nBandwitdh: 1\nSite: dummy-site\n"


def test_deleted():
    body = {"agent": "dummy-user", "host": DUMMY_HOST, "site": DUMMY_SITE}
    message = HostDeletedV2(body=body)
    message.validate()
    assert message.summary == "Host dummy-host has been deleted from site dummy-site by dummy-user"
    assert str(message) == "Host name: dummy-host\nCountry: US\nBandwitdh: 1\nSite: dummy-site\n"


def test_v1_added():
    body = {"host_id": DUMMY_HOST["id"], "site_id": DUMMY_SITE["id"], "bandwidth": 0, "asn": 0}
    message = HostAddedV1(body=body)
    message.validate()
    assert message.deprecated is True
    assert str(message) == f"Host on site {DUMMY_SITE['id']} has been added"


def test_v1_updated():
    body = {"host_id": DUMMY_HOST["id"], "site_id": DUMMY_SITE["id"], "bandwidth": 0, "asn": 0}
    message = HostUpdatedV1(body=body)
    message.validate()
    assert message.deprecated is True
    assert str(message) == f"Host on site {DUMMY_SITE['id']} has been updated"


def test_v1_deleted():
    body = {"host_id": DUMMY_HOST["id"], "site_id": DUMMY_SITE["id"], "bandwidth": 0, "asn": 0}
    message = HostDeletedV1(body=body)
    message.validate()
    assert message.deprecated is True
    assert str(message) == f"Host on site {DUMMY_SITE['id']} has been deleted"


def test_crawler_disabled():
    body = {
        "host": deepcopy(DUMMY_HOST),
        "site": DUMMY_SITE,
        "crawled_at": "2025-01-31T00:00:00+00:00",
        "logs_url": "http://example.com/logs",
        "reason": "dummy reason",
    }
    body["host"]["url"] = "http://example.com/hosts/42"
    message = HostCrawlerDisabledV1(body=body)
    message.validate()
    assert message.url == "http://example.com/hosts/42"
    assert message.agent_name is None
    assert message.usernames == ["dummy-admin"]
    assert message.summary == "Host dummy-host has been disabled by MirrorManager's crawler"
    assert (
        str(message)
        == """dummy reason

The host was crawled at 2025-01-31T00:00:00+00:00.
The crawl log can be found at http://example.com/logs
The host's page in MirrorManager can be found at http://example.com/hosts/42
"""
    )


def test_crawler_disabled_no_host_url():
    body = {
        "host": DUMMY_HOST,
        "site": DUMMY_SITE,
        "crawled_at": "2025-01-31T00:00:00+00:00",
        "logs_url": "http://example.com/logs",
        "reason": "dummy reason",
    }
    message = HostCrawlerDisabledV1(body=body)
    message.validate()
    assert (
        str(message)
        == """dummy reason

The host was crawled at 2025-01-31T00:00:00+00:00.
The crawl log can be found at http://example.com/logs
"""
    )
