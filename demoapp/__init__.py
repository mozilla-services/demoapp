from pyramid.config import Configurator
from demoapp.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('demoapp.views.my_view',
                    context='demoapp:resources.Root',
                    renderer='demoapp:templates/mytemplate.pt')
    config.add_static_view('static', 'demoapp:static', cache_max_age=3600)
    return config.make_wsgi_app()
