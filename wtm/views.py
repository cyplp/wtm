import urllib2

from lxml import etree

from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    home page
    """

    return {'project': 'wtm'}

@view_config(route_name='addContent', renderer='json')
def addContent(request):

    baseURL = 'http://www.overpass-api.de/api/interpreter'

    data = 'node(around:250.0,%s,%s)["amenity"="cafe"];out;' % (request.POST['lat'], request.POST['lon'])

    url = urllib2.Request(baseURL, data)

    xmlData = urllib2.urlopen(url).read()

    xml = etree.fromstring(xmlData)


    for node in xml.xpath('node/tag[@k="name"]'):
        print node.get('v')


    return ''
