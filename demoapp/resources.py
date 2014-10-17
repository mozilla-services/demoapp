# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/

from pyramid.security import Everyone, Authenticated, Allow


class Root(object):

    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, Authenticated, "authenticated"),
    ]

    def __init__(self, request):
        self.request = request
