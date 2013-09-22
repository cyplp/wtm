import urllib2

from lxml import etree

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry as gcr

settings = gcr().settings

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    home page
    """

    return {}

@view_config(route_name='addContent', renderer='json')
def addContent(request):
    """

    """

    xmlData = overpassRequest (request.POST['dist'],
                               request.POST['lat'],
                               request.POST['lon'])

    print xmlData
    xml = etree.fromstring(xmlData)

    names = [node.get('v') for node in xml.xpath('node/tag[@k="name"]')]
    print names

    return ''

def overpassRequest(dist, lat, lon):
    """
    """
    baseURL = settings['overpass_url']
    data = 'node(around:%s.0,%s,%s)["tourism"="museum"];out;' % (dist, lat, lon)
    url = urllib2.Request(baseURL, data)

    return  urllib2.urlopen(url).read()

