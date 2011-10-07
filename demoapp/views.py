
def get_config(request):
    return request.registry.settings.get('config')


def default_view(request):
    config = get_config(request)
    return config.get_map()
