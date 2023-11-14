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


class Industry(DjangoNode, NodeUtils):

    name = StringProperty()

    # Relationships
    company                = RelationshipFrom('.company.Company', 'IN_INDUSTRY')

    sector              = RelationshipTo('.sector.Sector', 'IN_SECTOR')


    class Meta:
        app_label = "fetch_api"

    @property
    def serialize(self):
        return {
            'node_properties': {
                   'name' : self.name,           
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
                'nodes_type': 'Sector',
                'nodes_related': self.serialize_relationships(self.sector.all()),
            },
        ]