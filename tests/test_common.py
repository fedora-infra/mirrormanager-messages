# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for common properties of the message schemas."""

from mirrormanager_messages.site import SiteDeletedV2

from .utils import DUMMY_SITE


def test_properties():
    """Assert some properties are correct."""
    body = {
        "agent": "dummy-user",
        "site": DUMMY_SITE,
    }
    message = SiteDeletedV2(body=body)
    assert message.app_name == "MirrorManager"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/mirrormanager.png"
