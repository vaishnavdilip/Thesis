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


class Country(DjangoNode):

    country = StringProperty()

    # Relationships
    company_in                = RelationshipTo('.company.Company', 'IN_COUNTRY')
    supplier_in               = RelationshipTo('.supplier.Supplier', 'IN_COUNTRY')
    parent_in                 = RelationshipTo('.parent.Parent', 'IN_COUNTRY')

    continent_of              = RelationshipFrom('.continent.Continent', 'IN_CONTINENT')


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
                'nodes_type': 'Continent',
                'nodes_related': self.serialize_relationships(self.continent_of.all()),
            },
        ]