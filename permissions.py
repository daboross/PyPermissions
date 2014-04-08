### Utility methods
def prepare(permission):
    """
    Prepares the given permission using unicode(permission).lower()
    @type permission: str
    @param permission: The permission to prepare
    """
    return str(permission).lower()


### Permission tree
class PermissionTree:
    def __init__(self):
        self._parent_tree = {}
        self._child_tree = {}

    def add_inheritance(self, parent, child):
        """
        @type child: unicode
        @type parent: unicode
        """
        parent = prepare(parent)
        child = prepare(child)
        if parent in self._child_tree:
            self._child_tree[parent].extend(child)
        else:
            self._child_tree[parent] = [child]

        if child in self._parent_tree:
            self._parent_tree[child].extend(parent)
        else:
            self._parent_tree[child] = [parent]

    def get_parents(self, permission):
        """

        @type permission: unicode
        """
        permission = prepare(permission)
        if permission not in self._parent_tree:
            return []

        return self._parent_tree[permission]

    def get_children(self, permission):
        """

        @type permission: unicode
        """
        permission = prepare(permission)
        if permission not in self._child_tree:
            return []

        return self._child_tree[permission]


### Initialize the default tree
PermissionTree.default_tree = PermissionTree()


class PermissionSet:
    """
    Represents a set of permissions.
    """

    def __init__(self, permission_tree=PermissionTree.default_tree):
        """
        Creates a new PermissionSet, default using the default_tree.
        Specify a PermissionTree if you would like to edit permission inheritance, or just modify
        PermissionTree.default_tree

        @param permission_tree: A permission tree to get inheriting permissions from
        @type permission_tree: PermissionTree
        """
        self.permissions = {}
        self._cache = {}
        self._tree = permission_tree

    def __cmp__(self, other):
        if not isinstance(other, PermissionSet):
            return self.__class__.__name__.__cmp__(other.__class__.__name__)
        return self.permissions.__cmp__(other.permissions)

    def __getitem__(self, item):
        return self.has(prepare(item))

    def __delitem__(self, key):
        self.remove(prepare(key))

    def __invert__(self):
        inverted_set = PermissionSet()
        for permission, value in self.permissions.iteritems():
            inverted_set.set(permission, value=not value, invalidate_cache=False)
        inverted_set.invalidate_cache()
        return inverted_set

    def __str__(self):
        return str(self.permissions)

    def invalidate_cache(self):
        """
        Invalidates the cache, useful when changing things in batch and using invalidate_cache=True.
        """
        self._cache = {}

    def remove(self, permission, invalidate_cache=True):
        """
        Removes all settings for a given permission.
        @type permission: unicode
        @type invalidate_cache: bool
        @param permission: The permission to remove
        @param invalidate_cache: Whether or not to invalidate the cache after performing this action. Only specify False
                if you are calling multiple changing methods and will call invalidate_cache afterwards
        """
        permission = prepare(permission)
        self.permissions.pop(permission, None)
        if invalidate_cache:
            self.invalidate_cache()

    def set(self, permission, value=True, invalidate_cache=True):
        """
        Adds or sets a permission in this PermissionSet.

        @type permission: unicode
        @type value: bool
        @type invalidate_cache: bool
        @param permission: The permission to set
        @param value: Whether to set this permission to True or False, defaulting to True
        @param invalidate_cache: Whether or not to invalidate the cache after performing this action. Only specify False
                if you are calling multiple changing methods and will call invalidate_cache afterwards
        """
        permission = prepare(permission)
        self.permissions[permission] = value
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
            self.set(prepare(permission), value=permissions[permission], invalidate_cache=False)
        if invalidate_cache:
            self.invalidate_cache()

    def _evaluate(self, permission):
        """
        Evaluates whether this PermissionSet has 'permission', defaulting to False.

        Will first check the cache and permission set for the permission, then each of permission's parents, and each
        of permission's parents' parents, until either a permission evaluates to True, or all parents are checked, and
        found to be false.
        Either way, the found value is stored in the cache, and then returned.

        This method will use the cache, make sure you have used invalidate_cache() after using any changing methods with
        the 'invalidate_cache=False' parameter.

        ** Warning **: This method may result in a stack overflow if the parent structure is circular

        @type permission: unicode
        @param permission: Permission string to check. Should be lowercase unicode.
        @return Whether or not the permission is set to true in this PermissionSet.
        """
        value = False

        if permission in self._cache:
            return self._cache[permission]

        if permission in self.permissions:
            value = self.permissions[permission]
        elif permission == "true":
            value = True
        else:
            parents = self._tree.get_parents(permission)
            for parent in parents:
                value = self._evaluate(parent)
                if value is True:
                    break

        self._cache[permission] = value
        return value

    def has(self, permission):
        """
        Evaluates whether this PermissionSet has 'permission', defaulting to False.

        Will first check the cache and permission set for the permission, then each of permission's parents, and each
        of permission's parents' parents, until either a permission evaluates to True, or all parents are checked, and
        found to be false.
        Either way, the found value is stored in the cache, and then returned.

        ** Warning **: This method may result in a stack overflow if the parent structure is circular

        This method will use the cache, make sure you have used invalidate_cache() after using any changing methods with
        the 'invalidate_cache=False' parameter.

        The 'permission' parameter is processed with unicode(permission).lower().

        @type permission: unicode
        @param permission: Permission string to check
        @return Whether or not the permission is set to true in this PermissionSet.
        """
        permission = prepare(permission)
        return self._evaluate(prepare(permission))