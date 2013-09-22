import urllib2

from lxml import etree

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry as gcr

from beaker.cache import cache_region

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

    return ''

@cache_region('short_term', 'overpass')
def overpassRequest(dist, lat, lon):
    """
    """
    #TODO beaker cache
    baseURL = settings['overpass_url']
    data = 'node(around:%s.0,%s,%s)["tourism"="museum"];out;' % (dist, lat, lon)
    url = urllib2.Request(baseURL, data)

    return  urllib2.urlopen(url).read()

