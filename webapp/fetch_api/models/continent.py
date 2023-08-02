from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty,
    
)
from django_neomodel import DjangoNode

from .nodeutils import NodeUtils


class Continent(DjangoNode):

    name = StringProperty()

    # Country Node

    country = RelationshipFrom('.country.Country', 'IN_COUNTRY')



    class Meta:
        app_label = "fetch_api"

    @property
    def serialize(self):
        return {
            'node_properties': {
                'name': self.name,         
            },
        }
    
    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Country',
                'nodes_related': self.serialize_relationships(self.country.all()),
            },
        ]