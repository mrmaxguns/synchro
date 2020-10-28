from .exceptions import SyncError


class ServerBackupShadow:
    def __init__(self, data):
        self.data = data
        self.version = 0

    def __str__(self):
        return "ServerBackupShadow"

    def __repr__(self):
        return f"<{self.__str__()} v{str(self.version)}>"


class Shadow:
    def __init__(self, data, version=None):
        self.data = data
        if version is None:
            self.version = [0, 0]  # client, server
        else:
            self.version = version

    def __str__(self):
        return "Shadow"

    def __repr__(self):
        version = ".".join([str(i) for i in self.version])
        return f"<{self.__str__()} v{version}>"


class ServerShadow(Shadow):
    def __init__(self, data, version=None):
        super().__init__(data, version=None)
        self.backup = ServerBackupShadow(data)

    def rollback(self):
        self.data = self.backup.data
        self.version[1] = self.backup.version
        return self.backup.version

    def update_backup(self):
        self.backup.data = self.data
        self.backup.version = self.version[1]
        return self.backup.version

    def __str__(self):
        return "ServerShadow"
