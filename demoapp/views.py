
from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid

from demoapp import api


@api(pattern='/hello', renderer='json', method='GET')
def hello(request):
    """ Blah.
    """
    return {'Hello': 'World'}

@api(pattern='/{username}/secret', renderer='json', method='GET')
def secret(request):
    username = authenticated_userid(request)
    if request.matchdict["username"] != username:
        raise Forbidden()
    return {"username": username}

