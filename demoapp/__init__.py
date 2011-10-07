from pyramid.config import Configurator
from demoapp.resources import Root
from demoapp.config import Config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config_file = settings.get('configuration')
    if config_file:
        settings['config'] = Config(config_file)

    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('demoapp.views.default_view',
                    context='demoapp:resources.Root',
                    renderer='json')

    config.add_static_view('static', 'demoapp:static', cache_max_age=3600)
    return config.make_wsgi_app()
