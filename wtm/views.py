import urllib2

from lxml import etree

from deform import Form

from pyramid.view import view_config

from wtm.schemas.home import HomeSchema

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    home page
    """
    homeForm = Form(HomeSchema(), buttons=('submit',), action=request.route_path('addContent'))

    return {'form': homeForm.render()}

@view_config(route_name='addContent', renderer='json')
def addContent(request):

    baseURL = 'http://www.overpass-api.de/api/interpreter'

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

