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


class Industry(DjangoNode):

    name = StringProperty()

    # Relationships
    company_in                = RelationshipTo('.company.Company', 'IN_INDUSTRY')
    supplier_in               = RelationshipTo('.supplier.Supplier', 'IN_INDUSTRY')
    parent_in                 = RelationshipTo('.parent.Parent', 'IN_INDUSTRY')

    sector_of              = RelationshipFrom('.sector.Sector', 'IN_SECTOR')


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
                'nodes_type': 'Suppplier',
                'nodes_related': self.serialize_relationships(self.supplier_in.all()),
            },
            {
                'nodes_type': 'Parent',
                'nodes_related': self.serialize_relationships(self.parent_in.all()),
            },
            {
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.company_in.all()),
            },
            {
                'nodes_type': 'Sector',
                'nodes_related': self.serialize_relationships(self.sector_of.all()),
            },
        ]