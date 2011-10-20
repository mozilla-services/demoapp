import os

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy

from demoapp.resources import Root
from mozsvc.config import Config


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
    config.include("pyramid_whoauth")

    # adds cornice
    config.include("cornice")

    # adds Mozilla default views
    config.include("mozsvc")

    config.scan("demoapp.views")
    return config.make_wsgi_app()
