from enum import IntEnum

class Roles(IntEnum):
    ADMIN_USERS = 1
    ADMIN_POSTS = 2
    USER_USERS = 3
    USER_POSTS = 4
    GUEST = 5


class Action(IntEnum):
    READ = 1
    WRITE = 2
    UPDATE = 3
    DELETE = 4


class Resource(IntEnum):
    USERS = 1
    POSTS = 2


# WILL REPLACE IT WITH A DATABASE OR AN EXTERNAL SERVICE LATER
DUMMY_USER_DATA = {
    "1234": {"username": "admin_user", "role": Roles.ADMIN_USERS},
    "5678": {"username": "admin_post", "role": Roles.ADMIN_POSTS},
    "9101": {"username": "user_user", "role": Roles.USER_USERS},
}


class AccessControl:
    @staticmethod
    def permissions():
        return {
            Roles.ADMIN_USERS: {
                Resource.USERS: {Action.READ, Action.WRITE, Action.UPDATE, Action.DELETE}
            },
            Roles.ADMIN_POSTS: {
                Resource.POSTS: {Action.READ, Action.WRITE, Action.UPDATE, Action.DELETE}
            },
            Roles.USER_USERS: {
                Resource.USERS: {Action.READ}
            },
            Roles.USER_POSTS: {
                Resource.POSTS: {Action.READ, Action.WRITE}
            },
            Roles.GUEST: {
                Resource.USERS: {Action.READ},
                Resource.POSTS: {Action.READ}
            },
        }

    @staticmethod
    def is_allowed(role: str, url: str, method: str) -> bool:
        role = AccessControl.__get_role_from_user_data({"role": role})
        if role is None:
            return False
        resource = AccessControl.__get_resource_from_path(url)
        action = AccessControl.__get_action_from_method(method)
        if resource is None or action is None:
            return False
        return action in AccessControl.permissions().get(role, {}).get(resource, set())
    
    @staticmethod
    def __get_resource_from_path(path: str) -> Resource | None:
        if "/users" in path:
            return Resource.USERS
        elif "/posts" in path:
            return Resource.POSTS
        return None
    
    @staticmethod
    def __get_action_from_method(method: str) -> Action | None:
        method = method.upper()
        if method == "GET":
            return Action.READ
        elif method == "POST":
            return Action.WRITE
        elif method == "PATCH":
            return Action.UPDATE
        elif method == "DELETE":    
            return Action.DELETE
        
    @staticmethod
    def __get_role_from_user_data(user_data: dict) -> Roles | None:
        role_str = DUMMY_USER_DATA.get(user_data.get("role"), {}).get("role")
        if role_str is None:
            return None
        return role_str
