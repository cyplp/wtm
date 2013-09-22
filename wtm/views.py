import urllib2

from lxml import etree

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry as gcr

from beaker.cache import cache_region

import requests

settings = gcr().settings

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
        current = {'name': name,
                   'urls' : [processingImg(name, result['url']) for result in seeksRequest(name)['snippets']]}
        places.append(current)

    return {'places': places}

@cache_region('short_term', 'image')
def processingImg(name, url):
    """
    """
    req = requests.get(url)

    tmp = req.content
    sha1 = hashlib.sha1()

    sha1.update(tmp)

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
