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


class Sector(DjangoNode, NodeUtils):

    name = StringProperty()

    # Country Node

    industry = RelationshipFrom('.industry.Industry', 'IN_SECTOR')



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
                'nodes_type': 'Industry',
                'nodes_related': self.serialize_relationships(self.industry.all()),
            },
        ]