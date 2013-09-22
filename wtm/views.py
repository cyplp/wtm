import urllib2
import hashlib
import datetime
import logging

from lxml import etree

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry as gcr

from beaker.cache import cache_region

import requests

settings = gcr().settings

es = settings['ES']

_logger = logging.getLogger('views')


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    home page
    """

    return {}

@view_config(route_name='addContent', renderer='templates/addContent.pt')
def addContent(request):
    """

    """

    xmlData = overpassRequest (request.POST['dist'],
                               request.POST['lat'],
                               request.POST['lon'])

    xml = etree.fromstring(xmlData)

    names = [node.get('v') for node in xml.xpath('node/tag[@k="name"]')]

    places = []
    for name in names:
        _logger.info("seeking %s", name)
        try:
            current = {'name': name,
                       'urls' : [processingImg(name, result['url'])
                                 for result in seeksRequest(name.encode('utf-8'))['snippets']]}
            places.append(current)
        except UnicodeEncodeError:
            _logger.error('unicode error %s', name)
            continue

    return {'places': places}

@cache_region('short_term', 'image')
def processingImg(name, url):
    """
    """
    _logger.info("processing %s", url)
    try:
        req = requests.get(url.encode('utf-8'))
    except UnicodeEncodeError:
        _logger.error('unicode error %s', url)
        return url

    _logger.info("got %s", url)

    tmp = req.content
    sha1 = hashlib.sha1()

    sha1.update(tmp)
    _logger.info("sha1 %s", sha1.hexdigest())
    es.put('wtm/images/'+sha1.hexdigest(),
           data={'url': url,
                 'name': name,
                 'user': False,
                 #'dt_insert': datetime.datetime.now()
                 })

    return url
@cache_region('short_term', 'overpass')
def overpassRequest(dist, lat, lon):
    """
    """
    #TODO beaker cache
    baseURL = settings['overpass_url']
    data = 'node(around:%s.0,%s,%s)["tourism"="museum"];out;' % (dist, lat, lon)
    url = urllib2.Request(baseURL, data)

    return  urllib2.urlopen(url).read()

@cache_region('short_term', 'seeks')
def seeksRequest(requestedTerm):
    """
    """
    payload = {'output': 'json',
               'q': requestedTerm}

    baseURL = settings['seeks_url']
    req = requests.get(baseURL+'/search_img', params=payload)

    return req.json()
