# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from .base import MirrorManagerMessage, SCHEMA_URL, SITE_SCHEMA


class SiteDeletedV1(MirrorManagerMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a site is deleted.
    """

    topic = "mirrormanager.site.deleted"
    deprecated = True
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a site is deleted",
        "type": "object",
        "properties": {
            "site_id": {"type": "number"},
            "site_name": {"type": "string"},
            "org_url": {"type": ["string", "null"], "format": "uri"},
        },
        "required": ["site_id", "site_name", "org_url"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return self.summary

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Site {name} ({id}) has been deleted".format(
            name=self.body["site_name"], id=self.body["site_id"]
        )


class SiteDeletedV2(MirrorManagerMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a site is deleted.
    """

    topic = "mirrormanager.site.deleted.v2"

    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a site is deleted",
        "type": "object",
        "properties": {"agent": {"type": "string"}, "site": SITE_SCHEMA},
        "required": ["agent", "site"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        lines = [self.summary]
        if self.body["site"]["org_url"]:
            lines.append(f"Org URL: {self.body['site']['org_url']}")
        return "\n".join(lines)

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Site {name} ({id}) has been deleted by {agent}".format(
            name=self.body["site"]["name"], id=self.body["site"]["id"], agent=self.body["agent"]
        )
