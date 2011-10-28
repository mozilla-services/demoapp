from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid

from cornice import Service


info_desc = """\
This service is useful to get and set data for a user.
"""


user_info = Service(name='users', path='/{username}/info',
                    description=info_desc)

_USERS = defaultdict(dict)


@user_info.get()
def get_info(request):
    """Returns the public information about a **user**.

    If the user does not exists, returns an empty dataset.
    """
    username = request.matchdict['username']
    return _USERS[username]


@user_info.post()
def set_info(request):
    """Set the public information for a **user**.

    You have to be that user, and *authenticated*.

    Returns *True* or *False*.
    """
    username = authenticated_userid(request)
    if request.matchdict["username"] != username:
        raise Forbidden()
    _USERS[username] = request.json_body
    return {'success': True}
