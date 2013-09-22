from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

from pyramid.threadlocal import get_current_registry



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    sessionFactory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)

    config = Configurator(settings=settings)

    config.include('pyramid_fanstatic')
    config.include('pyramid_beaker')
    config.include('pyramid_rawes')
    config.include('rebecca.fanstatic')

    config.set_session_factory(sessionFactory)

    settings['ES'] = config.get_rawes()
    get_current_registry().settings = settings

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('addContent', '/addContent')
    config.add_route('content', '/content/{imgID}')
    config.add_route('image', '/image/{imgID}')

    # print settings['resources'].split(',')
    # print [resource.strip() for resource in settings['resources'].split(',')]

    # config.add_fanstatic_resources([resource.strip() for resource in settings['resources'].split(',')], r'.*\.pt')
    config.scan()
    return config.make_wsgi_app()
