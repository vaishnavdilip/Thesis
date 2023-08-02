from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty,
    
)
from django_neomodel import DjangoNode
from .basenode import Base

from .nodeutils import NodeUtils


class Company(Base):

    parent                  = Relationship('.company.Company', 'ULTIMATE_PARENT_OF')


    ## Supplier Node

    supplier_to_supplier                = RelationshipTo('.supplier.Supplier', 'SUPPLIES')
    partner_to_supplier                 = RelationshipTo('.supplier.Supplier', 'PARTNERS')
    competitor_to_supplier              = RelationshipTo('.supplier.Supplier', 'COMPETES')
    parent_to_supplier                  = RelationshipTo('.supplier.Supplier', 'ULTIMATE_PARENT_OF')
    supplier_test_to_supplier           = RelationshipTo('.supplier.Supplier', 'SUPPLIES_TEST')
    supplier_train_to_supplier          = RelationshipTo('.supplier.Supplier', 'SUPPLIES_TRAIN')
    supplier_valid_to_supplier          = RelationshipTo('.supplier.Supplier', 'SUPPLIES_VALID')

    supplier_from_supplier                = RelationshipFrom('.supplier.Supplier', 'SUPPLIES')
    partner_from_supplier                 = RelationshipFrom('.supplier.Supplier', 'PARTNERS')
    competitor_from_supplier              = RelationshipFrom('.supplier.Supplier', 'COMPETES')
    parent_from_supplier                  = RelationshipFrom('.supplier.Supplier', 'ULTIMATE_PARENT_OF')
    supplier_test_from_supplier           = RelationshipFrom('.supplier.Supplier', 'SUPPLIES_TEST')
    supplier_train_from_supplier          = RelationshipFrom('.supplier.Supplier', 'SUPPLIES_TRAIN')
    supplier_valid_from_supplier          = RelationshipFrom('.supplier.Supplier', 'SUPPLIES_VALID')


    # Ultimate Parent Node

    supplier_to_parent                = RelationshipTo('.parent.Parent', 'SUPPLIES')
    partner_to_parent                 = RelationshipTo('.parent.Parent', 'PARTNERS')
    competitor_to_parent              = RelationshipTo('.parent.Parent', 'COMPETES')
    supplier_test_to_parent           = RelationshipTo('.parent.Parent', 'SUPPLIES_TEST')
    supplier_train_to_parent          = RelationshipTo('.parent.Parent', 'SUPPLIES_TRAIN')
    supplier_valid_to_parent          = RelationshipTo('.parent.Parent', 'SUPPLIES_VALID')

    supplier_from_parent                = RelationshipFrom('.parent.Parent', 'SUPPLIES')
    partner_from_parent                 = RelationshipFrom('.parent.Parent', 'PARTNERS')
    competitor_from_parent              = RelationshipFrom('.parent.Parent', 'COMPETES')
    parent_from_parent                  = RelationshipFrom('.parent.Parent', 'ULTIMATE_PARENT_OF')
    supplier_test_from_parent           = RelationshipFrom('.parent.Parent', 'SUPPLIES_TEST')
    supplier_train_from_parent          = RelationshipFrom('.parent.Parent', 'SUPPLIES_TRAIN')
    supplier_valid_from_parent          = RelationshipFrom('.parent.Parent', 'SUPPLIES_VALID')


    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Suppplier',
                'nodes_related': self.serialize_relationships(self.supplier.all()),
            },
            {
                'nodes_type': 'Parent',
                'nodes_related': self.serialize_relationships(self.parent.all()),
            },
            {
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.supplier_test_to_parent.all()),
            },
            {
                'nodes_type': 'Country',
                'nodes_related': self.serialize_relationships(self.country.all()),
            },
            {
                'nodes_type': 'Industry',
                'nodes_related': self.serialize_relationships(self.industry.all())
            },
        ]
