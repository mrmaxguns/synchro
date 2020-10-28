#!/usr/bin/env python3
"""
Synchro: python's differential synchronization library
------------------------------------------------------

Many collaboration tools include block-free real-time collaboration with the
help of differential synchronization. Diffsync is a way of synchronizing the
same document between multiple instances. Many text editors feature auto-save
with the help of diffsync.

The simple process relies on diffs and patches. A diff is a way of comparing
text and listing out all differences between the two texts. A patch is a way
of applying a diff to a text. A client and server both have shadows. Whenever
a change is made to the server or client document, the document is compared
with the shadow (the previous version of the document) and the diff is sent
to the other party (if the change is on the client side, the diff is sent to the
server, and vice versa). Diffsync also relies on backups and version numbers
to make sure no data is ever lost.

Managing server or client-side diffsync in python is very easy with the help
or synchro:

>>> from synchro import Server
>>>
>>> # The document is stored on the server
>>> s = Server("To be or not to be...")
>>>
>>> # Add a new client with the connection function:
>>> c = s.connection()
>>>
>>> # All data is returned as a JSON-parsable dictionary so that there is
>>> # no problem sending data to the client, such as JavaScript
>>> c
{'id': 1, 'data': 'To be or not to be...', 'version': [0, 0]}
>>>
>>> # This can be sent to your client for processing. The server generates a
>>> # new id for each connection as well as the current data, and version number
>>>
>>> # The client can send a response every period of time (such as 5 seconds)
>>> # The response must have information such as the id, version, edits and
>>> # diffs, to learn more, see the documentation

The server does all the heavy lifting for you. The server automatically deals
with backups, parses the versions, etc. If you are using a JavaScript front-end
you will need to implement the client-side code which should be relatively
simple.

If your client is a desktop client or GUI written in python, you can use the
``Client`` class. This class provides the client-side of the diff-sync ready
to go.

**Further reading: https://neil.fraser.name/writing/sync**
"""

__author__ = "Maxim R."
__version__ = "0.0.1"
__license__ = "MIT"

from .client import Client
from .server import Server
