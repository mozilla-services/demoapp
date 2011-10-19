import demoapp
#from cornice import make_main
import os

from webob.exc import HTTPNotFound, HTTPMethodNotAllowed

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import BeforeRender

from cornice.resources import Root
from cornice.config import Config
from cornice import util
from cornice.service import Service, get_service     # NOQA


def main(global_config, **settings):
    config_file = global_config['__file__']
    config_file = os.path.abspath(
                    os.path.normpath(
                    os.path.expandvars(
                        os.path.expanduser(
                        config_file))))

    settings['config'] = config = Config(config_file)
    conf_dir, _ = os.path.split(config_file)

    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory=Root, settings=settings,
                            authorization_policy=authz_policy)

    # add auth via repoze.who
    # eventually the app will have to do this explicitly
    config.include("cornice.auth.whoauth")

    # adds cornice
    config.include("cornice")

    config.scan("demoapp.views")
    return config.make_wsgi_app()
