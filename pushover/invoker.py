#!/usr/bin/env python
import os

import requests

from pushover import po_params


class PushoverError(Exception): pass


class PushoverMessage:
    """
    Used for storing message specific data.
    """

    def __init__(self, message):
        """
        Creates a PushoverMessage object.
        """
        self.vars = {}
        self.files = {}
        self.vars[po_params.MESSAGE] = message

    def set_data(self, key, value):
        """
        Sets the value of a field "key" to the value of "value".
        """
        if value is not None:
            self.vars[key] = value

    def set_attachment(self, value):
        """
        Sets the value of a field "key" to the value of "value".
        """
        if value is not None:
            self.files[po_params.ATTACHMENT] = value

    def get_vars(self):
        """
        Returns a dictionary with the values for the specified message.
        """
        return self.vars

    def get_files(self):
        """
        Returns a dictionary with the values for the specified message.
        """
        return self.files

    def user(self, user_token, user_device=None):
        """
        Sets a single user to be the recipient of this message with token "user_token" and device "user_device".
        """
        self.set_data(po_params.USER, user_token)
        self.set_data(po_params.DEVICE, user_device)

    def __str__(self):
        return "PushoverMessage: " + str(self.vars)


class Pushover:
    """
    Creates a Pushover handler.

    Usage:

        po = Pushover("My App Token")
        po.user("My User Token", "My User Device Name")

        msg = po.msg("Hello, World!")

        po.send(msg)

    """

    PUSHOVER_ENDPOINT = "https://api.pushover.net/1/messages.json"
    PUSHOVER_CONTENT_TYPE = {"Content-type": "application/x-www-form-urlencoded"}

    def __init__(self, token=None):
        """
        Creates a Pushover object.
        """

        if token is None:
            raise PushoverError("No token supplied.")
        else:
            self.token = token
            self.user_token = None
            self.user_device = None
            self.messages = []

    def msg(self, message):
        """
        Creates a PushoverMessage object. Takes one "message" parameter (the message to be sent).
        Returns with PushoverMessage object (msg).
        """

        message = PushoverMessage(message)
        self.messages.append(message)
        return message

    def send(self, message):
        """
        Sends a specified message with id "message" or as object.
        """
        if type(message) is PushoverMessage:
            return self._send(message)
        else:
            raise PushoverError("Wrong type passed to Pushover.send()!")

    def sendall(self):
        """
        Sends all PushoverMessage's owned by the Pushover object.
        """

        response = []
        for message in self.messages:
            response.append(self._send(message))
        return response

    def user(self, user_token, user_device=None):
        """
        Sets a single user to be the recipient of all messages created with this Pushover object.
        """

        self.user_token = user_token
        self.user_device = user_device

    def _send(self, message):
        """
        Sends the specified PushoverMessage object via the Pushover API.
        """

        kwargs = message.get_vars()
        kwargs[po_params.TOKEN] = self.token

        assert po_params.MESSAGE in kwargs
        assert self.token is not None

        if not po_params.USER in kwargs:
            if self.user is not None:
                kwargs[po_params.USER] = self.user_token
                if self.user_device is not None:
                    kwargs[po_params.DEVICE] = self.user_device
            else:
                kwargs[po_params.USER] = os.environ['PUSHOVER_USER']

        kwargs[po_params.USER] = os.environ['PUSHOVER_USER']
        kwargs[po_params.TOKEN] = os.environ['PUSHOVER_API_TOKEN']

        post = requests.post(Pushover.PUSHOVER_ENDPOINT, data=kwargs, files=message.get_files())

        if post.status_code != 200:
            raise PushoverError(post.text)
        else:
            return post.text
