import os
from pyramid.config import Configurator
from demoapp.resources import Root
from demoapp.config import Config

from pyramid.view import view_config
from pyramid.interfaces import IRoutesMapper
import venusian

def add_apidoc(config, pattern, docstring, renderer):
    apidocs = config.registry.settings.setdefault('apidocs', {})
    info = apidocs.setdefault(pattern, {})
    info['docstring'] = docstring
    info['renderer'] = renderer


class api(object):
    def __init__(self, **kw):
        self.route_pattern = kw.pop('pattern')
        self.route_method = kw.pop('method', None)
        self.kw = kw

    def __call__(self, func):
        kw = self.kw.copy()
        docstring = func.__doc__
        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            renderer = self.kw.get('renderer')
            route_name = func.__name__
            route_method = self.route_method
            config.add_apidoc((self.route_pattern, route_method),
                              docstring, renderer)
            config.add_route(route_name, self.route_pattern,
                             request_method=route_method)
            config.add_view(view=ob, route_name=route_name, **kw)

        info = venusian.attach(func, callback, category='pyramid')

        if info.scope == 'class':
            # if the decorator was attached to a method in a class, or
            # otherwise executed at class scope, we need to set an
            # 'attr' into the settings if one isn't already in there
            if kw['attr'] is None:
                kw['attr'] = func.__name__

        kw['_info'] = info.codeinfo # fbo "action_method"
        return func


@view_config(route_name='apidocs', renderer='apidocs.mako')
def apidocs(request):
    routes = []
    mapper = request.registry.getUtility(IRoutesMapper)
    for k, v in request.registry.settings['apidocs'].items():
        routes.append((k, v))
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
