import os

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from mozsvc.config import Config

from demoapp.resources import Root


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

    # adds authorization
    # option 1: auth via repoze.who
    config.include("pyramid_whoauth")
    # option 2: auth based on IP address
    #config.include("pyramid_ipauth")

    # adds cornice
    config.include("cornice")

    # adds Mozilla default views
    config.include("mozsvc")

    # adds application-specific views
    config.add_route("whoami", "/whoami")
    config.scan("demoapp.views")
    return config.make_wsgi_app()
