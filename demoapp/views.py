from demoapp import api


@api('/hello', renderer='json')
def hello(request):
    """ Blah.
    """
    return {'Hello': 'World'}
