from pyramid.config import Configurator
from demoapp.resources import Root
from demoapp.config import Config


# add your functions here
URLS = (
 ('/', 'demoapp.views.default_view', 'json'),
 ('/config', 'demoapp.views.default_view', 'json'),
)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config_file = settings.get('configuration')
    if config_file:
        settings['config'] = Config(config_file)

    config = Configurator(root_factory=Root, settings=settings)
    for index, (url, view, renderer) in enumerate(URLS):
        name = 'view%d' % index
        config.add_route(name, url, renderer=renderer, view=view)

    config.add_static_view('static', 'demoapp:static', cache_max_age=3600)
    return config.make_wsgi_app()
