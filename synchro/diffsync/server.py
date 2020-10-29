from itertools import filterfalse, count

from .shadow import Shadow, ServerShadow
from ..diffs import diff as default_diff
from ..diffs import patch as default_patch
from ..exceptions import SyncError

from copy import deepcopy


class DSServer:
    def __init__(self, data=None, diff=default_diff, patch=default_patch):
        if data is None:
            self.data = ""
        else:
            self.data = data
        self._clients = set()
        self._client_shadows = {}
        self._diff = diff
        self._patch = patch

    def connection(self):
        # generate the client and shadow
        client_id = self._get_next_client()
        shadow = ServerShadow(self.data)

        self._clients.add(client_id)
        self._client_shadows[client_id] = shadow

        # return client information
        return {
            "id": client_id,
            "data": shadow.data,
            "version": deepcopy(shadow.version),
            # "diff": self._diff,
            # "patch": self._patch,
        }

    def receive(self, message):
        # receive and apply the edits
        client_id = message["id"]
        if client_id not in self._clients:
            raise SyncError(f"a client with the id of '{str(id)}' does not exist")

        version = message["version"]
        edits = message["edits"]
        client_shadow = self._client_shadows[client_id]

        rollback = False
        if version != client_shadow.version:
            # version confilt, packet lost
            client_shadow.rollback()
            rollback = True

        # apply each edit
        for edit in edits:
            if edit["version"][0] >= client_shadow.version[0]:
                # patch the changes
                client_shadow.data = self._patch(edit["diff"], client_shadow.data)
                self.data = self._patch(edit["diff"], self.data)

                # update version number
                client_shadow.version[0] = edit["version"][0]

        # increment client version server-side
        client_shadow.version[0] += 1

        # run backup
        client_shadow.update_backup()

        # return a response
        edits = {
            # "diff": self._diff(self.data, client_shadow.data),
            "diff": self._diff(client_shadow.data, self.data),
            "version": deepcopy(client_shadow.version),
            "rollback": rollback,
        }

        # increment version number
        client_shadow.version[1] += 1

        return edits

    def receive_a(self, id, version, edits):
        return self.receive({"id": id, "version": version, "edits": edits})

    def close_connection(self, id):
        if id not in self._clients:
            raise ValueError(f"a client with the id of '{str(id)}' does not exist")
        self._clients.remove(id)
        self._client_shadows.pop(id)
        return id

    def reset(self):
        client_ids = deepcopy(self._clients)
        self._clients.clear()
        self._client_shadows.clear()
        return client_ids

    def _get_next_client(self):
        # get first value not found in the _clients set
        return next(filterfalse(self._clients.__contains__, count(1)))

    def __str__(self):
        return "DSServer"

    def __repr__(self):
        return f"<{self.__str__()}>"
