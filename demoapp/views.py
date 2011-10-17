from collections import defaultdict
from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid

from cornice import Service

user_info = Service(name='users', path='/{username}/info')
_USERS = defaultdict(dict)


@user_info.api(method='GET')
def get_info(request):
    """Returns the public information about a user.

    If the user does not exists, returns an empty dataset.
    """
    username = request.matchdict['username']
    return _USERS[username]


@user_info.api(method='POST')
def set_info(request):
    """Set the public information for a user.

    You have to be that user, and authenticated.

    Returns True or False.
    """
    username = authenticated_userid(request)
    if request.matchdict["username"] != username:
        raise Forbidden()
    _USERS[username] = request.json_body
    return True
