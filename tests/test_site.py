# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from mirrormanager_messages.site import SiteDeletedV1, SiteDeletedV2

from .utils import DUMMY_SITE


def test_minimal_deleted():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {"agent": "dummy-user", "site": DUMMY_SITE}
    message = SiteDeletedV2(body=body)
    message.validate()
    assert message.url is None
    assert message.agent_name == "dummy-user"
    assert message.usernames == ["dummy-user"]
    assert message.agent_avatar == (
        "https://seccdn.libravatar.org/avatar/"
        "18e8268125372e35f95ef082fd124e9274d46916efe2277417fa5fecfee31af1"
        "?s=64&d=retro"
    )
    expected_summary = (
        f"Site {DUMMY_SITE['name']} ({DUMMY_SITE['id']}) has been deleted by dummy-user"
    )
    assert message.summary == expected_summary
    assert str(message) == expected_summary


def test_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {
        "agent": "dummy-user",
        "site": {"id": 1},
    }
    message = SiteDeletedV2(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_minimal_deleted_with_org_url():
    dummy_site = DUMMY_SITE.copy()
    dummy_site["org_url"] = "http://dummy.example.com"
    body = {"agent": "dummy-user", "site": dummy_site}
    message = SiteDeletedV2(body=body)
    message.validate()
    assert str(message) == (
        f"Site {DUMMY_SITE['name']} ({DUMMY_SITE['id']}) has been deleted by dummy-user\n"
        "Org URL: http://dummy.example.com"
    )


def test_v1_deleted():
    body = {
        "site_id": DUMMY_SITE["id"],
        "site_name": DUMMY_SITE["name"],
        "org_url": DUMMY_SITE["org_url"],
    }
    message = SiteDeletedV1(body=body)
    message.validate()
    assert message.deprecated is True
    assert str(message) == f"Site {DUMMY_SITE['name']} ({DUMMY_SITE['id']}) has been deleted"
