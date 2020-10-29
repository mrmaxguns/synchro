from .shadow import Shadow
from ..diffs import diff as default_diff
from ..diffs import patch as default_patch

from copy import deepcopy


class DSClient:
    def __init__(self, id, data, version, diff=default_diff, patch=default_patch):
        self.id = id
        self._data = data
        self._shadow = Shadow(data=data, version=version)
        self._diff = default_diff
        self._patch = default_patch
        self._edit_stack = []

    def commit(self, data):
        # update the data
        self._data = data

        # create the diff
        diff = self._diff(self._shadow.data, self._data)

        # update the shadow
        self._shadow.data = data

        # add the edit to the stack and generate the edits
        self._edit_stack.append({"version": deepcopy(self._shadow.version), "diff": diff})
        edits = {
            "id": self.id,
            "version": deepcopy(self._shadow.version),
            "edits": deepcopy(self._edit_stack),
        }

        # increment the client version number
        self._shadow.version[0] += 1

        return edits

    def update(self, data):
        diff, version = data["diff"], data["version"]

        # clear the edit stack on successful update
        self._edit_stack.clear()

        # update server version number signifying that we got a response
        # from the server
        self._shadow.version[1] += 1

        # patch the changes
        self._shadow.data = self._patch(diff, self._shadow.data)
        self._data = self._patch(diff, self._data)

    def update_a(self, diff, version):
        return self.update({"diff": diff, "version": version})

    @property
    def data(self):
        # make sure data cannot be directly edited
        return self._data

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"<DSClient {self.__str__()}>"
