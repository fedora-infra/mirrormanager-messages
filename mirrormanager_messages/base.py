# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from fedora_messaging import message


SCHEMA_URL = "http://fedoraproject.org/message-schema/"

SITE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "org_url": {"type": ["string", "null"], "format": "uri"},
    },
    "required": ["id", "name", "org_url"],
}


class MirrorManagerMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by MirrorManager.
    """

    @property
    def app_name(self):
        return "MirrorManager"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/mirrormanager.png"

    @property
    def agent_name(self):
        """The username of the user who initiated the action that generated this message."""
        return self.body.get("agent")

    @property
    def usernames(self):
        """List of users affected by the action that generated this message."""
        return [self.agent_name]
