from demoapp import api


@api(pattern='/hello', renderer='json', method='GET')
def hello(request):
    """ Blah.
    """
    return {'Hello': 'World'}
