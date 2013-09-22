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

    baseURL = settings['overpass_url']

    data = 'node(around:%s.0,%s,%s)["amenity"="cafe"];out;' % (request.POST['dist'],
                                                               request.POST['lat'],
                                                               request.POST['lon'])

    print data

    url = urllib2.Request(baseURL, data)

    xmlData = urllib2.urlopen(url).read()

    xml = etree.fromstring(xmlData)


    for node in xml.xpath('node/tag[@k="name"]'):
        print node.get('v')


    return ''

