
from pyramid.security import Everyone, Authenticated, Allow


class Root(object):

    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, Authenticated, "authenticated"),
    ]

    def __init__(self, request):
        self.request = request
