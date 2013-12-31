class PermissionSet:
    def __init__(self):
        self.permissions = {}
        self.cache = {}

    def add(self, permission, value=True):
        self.permissions[permission] = value
        cache = {}

    def add_batch(self, ):
        pass

    def has(self, permission):
        pass