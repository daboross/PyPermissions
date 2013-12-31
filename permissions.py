class PermissionSet:
    """
    Represents a set of permissions.
    """

    def __init__(self):
        self.permissions = {}
        self.cache = {}

    def __cmp__(self, other):
        if not isinstance(other, PermissionSet):
            return False
        return self.permissions.__cmp__(other.permissions)

    def __getitem__(self, item):
        return self.has(item)

    def __invert__(self):
        inverted_set = PermissionSet()
        for permission, value in self.permissions.iteritems():
            inverted_set.set(permission, value=not value, invalidate_cache=False)
        inverted_set.invalidate_cache()
        return inverted_set

    def __str__(self):
        return str(self.permissions)

    def __unicode__(self):
        return unicode(self.permissions)

    def invalidate_cache(self):
        """
        Invalidates the cache, useful when changing things in batch and using invalidate_cache=True.
        """
        self.cache = {}

    def remove(self, permission):
        """
        Removes all settings for a given permission.
        @type permission: str
        @param permission: The permission to remove
        """
        self.permissions.pop(permission.lower(), None)
        self.invalidate_cache()

    def set(self, permission, value=True, invalidate_cache=True):
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

    def set_batch(self, permissions, invalidate_cache=True):
        """
        Adds a batch of permissions to this PermissionSet.

        @type permissions: dict
        @type invalidate_cache: bool
        @param permissions: Dictionary from str permission to boolean value
        @param invalidate_cache; Whether or not to invalidate the cache after performing this action. Only specify False
                if you are calling multiple changing methods and will call invalidate_cache() afterwards
        """
        for permission in permissions.keys():
            self.set(permission, value=permissions[permission], invalidate_cache=False)
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

        @type permission: str | unicode
        @param permission: Permission string to check
        @return Whether or not the permission is set to true in this PermissionSet.
        """
        permission = permission.lower()
        while permission not in self.permissions:
            if '.' in permission:
                permission = permission.rsplit('.', 1)[0] + "^all"
            else:
                return False

        return self.permissions[permission]

    def has(self, permission):
        """
        Evaluates whether this PermissionSet has the given permission, defaulting to False if not set.
        Will check each .* sub permission until the permission contains no '.'s.

        For example, if given 'plugin.permission.give', will first check 'plugin.permission.give', then
        'plugin.permission.*', then 'plugin.*'. If any of them evaluate to False or True, that is returned. If none of
        those permissions are set, False is returned.

        This method will use the cache, make sure you have used invalidate_cache() after using any changing methods with
        the 'invalidate_cache=False' parameter.

        @type permission: str | unicode
        @param permission: Permission string to check
        @return Whether or not the permission is set to true in this PermissionSet.
        """
        if not (isinstance(permission, str) or isinstance(permission, unicode)):
            return False

        if permission in self.cache:
            return self.cache[permission]
        else:
            value = self.evaluate(permission)
            self.cache[permission] = value
            return value
