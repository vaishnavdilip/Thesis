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


class Country(DjangoNode, NodeUtils):

    country = StringProperty()

    # Relationships
    company                = RelationshipFrom('.company.Company', 'IN_COUNTRY')

    continent              = RelationshipTo('.continent.Continent', 'IN_CONTINENT')


    class Meta:
        app_label = "fetch_api"

    @property
    def serialize(self):
        return {
            'node_properties': {
                   'country' : self.country,           
            },
        }
    
    @property
    def serialize_relationships(self):
        return [
            {
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.company.all()),
            },
            {
                'nodes_type': 'Continent',
                'nodes_related': self.serialize_relationships(self.continent.all()),
            },
        ]