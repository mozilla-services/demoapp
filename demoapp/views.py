

def get_config(request):
    return request.registry.settings.get('config')


def heartbeat(request):
    # checks the server's state -- if wrong, return a 503 here
    return 'OK'


def manage(request):
    config = get_config(request)
    return {'config': config}


def hello(request):
    return {'Hello': 'World'}
