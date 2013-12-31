class PermissionSet:
    def __init__(self):
        self.permissions = {}
        self.cache = {}

    def invalidate_cache(self):
        self.cache = {}

    def remove(self, permission):
        """
        Removes all settings for a given permission.
        @type permission: str
        @param permission: The permission to remove
        """
        self.permissions.pop(permission.lower(), None)
        self.invalidate_cache()

    def add(self, permission, value=True, invalidate_cache=True):
        """
        Adds or sets a permission in this PermissionSet.

        @param permission: The permission to set
        @param value: Whether to set this permission to True or False, defaulting to True
        @param invalidate_cache: Whether or not to invalidate the cache after performing this action. Only specify False
                if you are calling multiple changing methods and will call invalidate_cache afterwards
        """
        self.permissions[permission.lower()] = value
        if invalidate_cache:
            self.invalidate_cache()

    def add_batch(self, permissions, invalidate_cache=True):
        """
        Adds a batch of permissions to this PermissionSet.

        @type permissions: dict
        @type invalidate_cache: bool
        @param permissions: Dictionary from str permission to boolean value
        @param invalidate_cache; Whether or not to invalidate the cache after performing this action. Only specify False
                if you are calling multiple changing methods and will call invalidate_cache() afterwards
        """
        for permission in permissions.keys():
            self.add(permission, value=permissions[permission], invalidate_cache=False)
        if invalidate_cache:
            self.invalidate_cache()

    def evaluate(self, permission):
        """
        Evaluates whether this PermissionSet has 'permission', defaulting to False if not set.
        Will check each .* sub permission until the permission contains no '.'s.

        For example, if given 'plugin.permission.give', will first check 'plugin.permission.give', then
        'plugin.permission.*', then 'plugin.*'. If any of them evaluate to False or True, that is returned. If none of
        those permissions are set, False is returned.

        This method does not use the cache, you should use has for permission checking

        @type permission: str
        @param permission: Permission string to check
        @return Whether or not the permission is set to true in this PermissionSet.
        """
        value = self.permissions[permission]
        while value is None:
            if '.' in permission:
                permission = permission.rsplit('.', 2)[0]
                value = self.permissions[permission]
            else:
                return False

        return value

    def has(self, permission):
        """
        Evaluates whether this PermissionSet has 'permission', defaulting to False if not set.
        Will check each .* sub permission until the permission contains no '.'s.

        For example, if given 'plugin.permission.give', will first check 'plugin.permission.give', then
        'plugin.permission.*', then 'plugin.*'. If any of them evaluate to False or True, that is returned. If none of
        those permissions are set, False is returned.

        This method will use the cache, make sure you have used invalidate_cache() after using any changing methods with
        the 'invalidate_cache=False' parameter.

        @type permission: str
        @param permission: Permission string to check
        @return Whether or not the permission is set to true in this PermissionSet.
        """
        value = self.cache[permission]
        if value is None:
            value = self.evaluate(permission)
            self.cache[permission] = value
        return value
