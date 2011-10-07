import os
from pyramid.config import Configurator
from demoapp.resources import Root
from demoapp.config import Config

HERE = os.path.dirname(__file__)

# add your functions here
URLS = (
 ('/hello', 'demoapp.views.hello', 'json'),
)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config_file = settings.get('configuration')
    if config_file:
        settings['config'] = Config(config_file)


    config = Configurator(root_factory=Root, settings=settings)
    # adding default views: __heartbeat__, __apis__
    config.add_route('heartbeat', '/__heartbeat__',
                     renderer='string',
                     view='demoapp.views.heartbeat')

    config.add_route('manage', '/__manage__',
                     renderer='manage.mako',
                     view='demoapp.views.manage')

    # adding user-defined routes
    for index, (url, view, renderer) in enumerate(URLS):
        name = 'view%d' % index
        config.add_route(name, url, renderer=renderer, view=view)

    config.add_static_view('static', 'demoapp:static', cache_max_age=3600)
    return config.make_wsgi_app()
