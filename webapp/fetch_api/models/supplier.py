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
from .basenode import Base


class Supplier(Base):

    parent                  = Relationship('.supplier.Supplier', 'ULTIMATE_PARENT_OF')


    ## Company Node

    supplier_to_company                = RelationshipTo('.company.Company', 'SUPPLIES')
    partner_to_company                 = RelationshipTo('.company.Company', 'PARTNERS')
    competitor_to_company              = RelationshipTo('.company.Company', 'COMPETES')
    parent_to_company                  = RelationshipTo('.company.Company', 'ULTIMATE_PARENT_OF')
    supplier_test_to_company           = RelationshipTo('.company.Company', 'SUPPLIES_TEST')
    supplier_train_to_company          = RelationshipTo('.company.Company', 'SUPPLIES_TRAIN')
    supplier_valid_to_company          = RelationshipTo('.company.Company', 'SUPPLIES_VALID')

    supplier_from_company                = RelationshipFrom('.company.Company', 'SUPPLIES')
    partner_from_company                 = RelationshipFrom('.company.Company', 'PARTNERS')
    competitor_from_company              = RelationshipFrom('.company.Company', 'COMPETES')
    parent_from_company                  = RelationshipFrom('.company.Company', 'ULTIMATE_PARENT_OF')
    supplier_test_from_company           = RelationshipFrom('.company.Company', 'SUPPLIES_TEST')
    supplier_train_from_company          = RelationshipFrom('.company.Company', 'SUPPLIES_TRAIN')
    supplier_valid_from_company          = RelationshipFrom('.company.Company', 'SUPPLIES_VALID')


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
                'nodes_related': self.serialize_relationships(self.supplier_to_company.all()),
            },
            {
                'nodes_type': 'Parent',
                'nodes_related': self.serialize_relationships(self.parent.all()),
            },
            {
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.supplier_from_company.all()),
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
