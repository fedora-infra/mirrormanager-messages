# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from .base import MirrorManagerMessage, SCHEMA_URL, SITE_SCHEMA


HOST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "country": {"type": "string"},
        "bandwidth": {"type": ["number", "null"]},
        "asn": {"type": ["number", "null"]},
        "url": {"type": "string"},
    },
    "required": ["id", "name", "country", "bandwidth", "asn"],
}

HOST_SCHEMA_V1 = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "site_id": {"type": "number"},
        "host_id": {"type": "number"},
        "bandwidth": {"type": ["number", "null"]},
        "asn": {"type": ["number", "null"]},
    },
    "required": ["site_id", "host_id", "bandwidth", "asn"],
}


class HostMessageV1(MirrorManagerMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager related to hosts.
    """

    deprecated = True

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return self.summary


class HostMessageV2(MirrorManagerMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager related to hosts.
    """

    _BODY_SCHEMA: typing.ClassVar = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {"agent": {"type": "string"}, "host": HOST_SCHEMA, "site": SITE_SCHEMA},
        "required": ["agent", "host", "site"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return (
            f"Host name: {self.body['host']['name']}\n"
            f"Country: {self.body['host']['country']}\n"
            f"Bandwitdh: {self.body['host']['bandwidth']}\n"
            f"Site: {self.body['site']['name']}\n"
        )

    @property
    def usernames(self):
        """List of users affected by the action that generated this message."""
        names = set(self.body["site"].get("admins", []))
        if self.agent_name:
            names.add(self.agent_name)
        return list(sorted(names))

    @property
    def url(self):
        return self.body["host"].get("url")


class HostAddedV1(HostMessageV1):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a new host is added.
    """

    topic = "mirrormanager.host.added"
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        **HOST_SCHEMA_V1,
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return f"Host on site {self.body['site_id']} has been added"


class HostAddedV2(HostMessageV2):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a new host is added.
    """

    topic = "mirrormanager.host.added.v2"

    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a host is added",
        **HostMessageV2._BODY_SCHEMA,
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Host {host_name} has been added to site {site_name} by {agent}".format(
            host_name=self.body["host"]["name"],
            site_name=self.body["site"]["name"],
            agent=self.body["agent"],
        )


class HostDeletedV1(HostMessageV1):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a new host is deleted.
    """

    topic = "mirrormanager.host.deleted"
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        **HOST_SCHEMA_V1,
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return f"Host on site {self.body['site_id']} has been deleted"


class HostDeletedV2(HostMessageV2):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a new host is deleted.
    """

    topic = "mirrormanager.host.deleted.v2"

    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a host is deleted",
        **HostMessageV2._BODY_SCHEMA,
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Host {host_name} has been deleted from site {site_name} by {agent}".format(
            host_name=self.body["host"]["name"],
            site_name=self.body["site"]["name"],
            agent=self.body["agent"],
        )


class HostUpdatedV1(HostMessageV1):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a new host is updated.
    """

    topic = "mirrormanager.host.updated"
    deprecated = True
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a host is updated",
        **HOST_SCHEMA_V1,
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return f"Host on site {self.body['site_id']} has been updated"


class HostUpdatedV2(HostMessageV2):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a new host is updated.
    """

    topic = "mirrormanager.host.updated.v2"

    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a host is updated",
        **HostMessageV2._BODY_SCHEMA,
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Host {host_name} in site {site_name} has been updated by {agent}".format(
            host_name=self.body["host"]["name"],
            site_name=self.body["site"]["name"],
            agent=self.body["agent"],
        )


class HostCrawlerDisabledV1(HostMessageV2):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager when a host is disabled by the crawler.
    """

    topic = "mirrormanager.crawler.host.disabled.v1"

    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a host is disabled by the crawler",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "host": HOST_SCHEMA,
            "site": SITE_SCHEMA,
            "crawled_at": {"type": "string"},
            "logs_url": {"type": "string"},
            "reason": {"type": "string"},
        },
        "required": ["host", "site", "crawled_at", "logs_url", "reason"],
    }

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Host {host_name} has been disabled by MirrorManager's crawler".format(
            host_name=self.body["host"]["name"],
        )

    def __str__(self):
        """Return a full description of the message (email body)."""
        content = f"""{self.body['reason']}

The host was crawled at {self.body['crawled_at']}.
The crawl log can be found at {self.body['logs_url']}
"""
        if self.body["host"].get("url"):
            content += "The host's page in MirrorManager can be found at "
            content += self.body["host"]["url"]
            content += "\n"
        return content
