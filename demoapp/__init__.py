import os
from pyramid.config import Configurator
from demoapp.resources import Root
from demoapp.config import Config

from pyramid.view import view_config
from pyramid.interfaces import IRoutesMapper


def add_apidoc(config, url, docstring, renderer):
    apidocs = config.registry.settings.setdefault('apidocs', {})
    info = apidocs.setdefault(url, {})
    info['docstring'] = docstring
    info['renderer'] = renderer


class api(view_config):
    def __init__(self, route, **kw):
        kw['route_name'] = route
        view_config.__init__(self, **kw)
        self._route = route

    def __call__(self, func):
        route = self._route
        del self._route
        view_config.__call__(self, func)
        docstring = func.__doc__

        def callback(context, name, ob):
            config = context.config
            config.add_route(route, route)
            renderer = self.renderer
            route_name = self.route_name
            add_apidoc(config, route_name, docstring, renderer)

        self.venusian.attach(func, callback, category='pyramid')
        return func


@view_config(route_name='apidocs', renderer='apidocs.mako')
def apidocs(request):
    routes = []
    mapper = request.registry.getUtility(IRoutesMapper)
    for k, v in request.registry.settings['apidocs'].items():
        route = mapper.get_route(k)
        if route is not None:
            routes.append((route.pattern, v))
    return {'routes': routes}


HERE = os.path.dirname(__file__)


def get_config(request):
    return request.registry.settings.get('config')


def heartbeat(request):
    # checks the server's state -- if wrong, return a 503 here
    return 'OK'


def manage(request):
    config = get_config(request)
    return {'config': config}


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
                     view='demoapp.heartbeat')

    config.add_route('manage', '/__config__',
                     renderer='config.mako',
                     view='demoapp.manage')

    config.add_static_view('static', 'demoapp:static', cache_max_age=3600)
    config.add_directive('add_apidoc', add_apidoc)
    config.add_route('apidocs', '/__apidocs__')
    config.scan()
    return config.make_wsgi_app()
