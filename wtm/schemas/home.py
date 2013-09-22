import colander

from deform import widget

class HomeSchema(colander.MappingSchema):
    lat = colander.SchemaNode(colander.Float(),
                              widget=widget.HiddenWidget(),
                              oid='lat'
                              )
    lon = colander.SchemaNode(colander.Float(),
                              widget=widget.HiddenWidget(),
                              oid='lon'
                              )



    dist = colander.SchemaNode(colander.Integer(),
                               validator=colander.Range(50,30000),
                               oid='dist')
