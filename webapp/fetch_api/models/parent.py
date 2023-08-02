from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty
    )
from django_neomodel import DjangoNode
from .basenode import Base

from .nodeutils import NodeUtils


class Parent(Base):

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
    supplier_test_from_company           = RelationshipFrom('.company.Company', 'SUPPLIES_TEST')
    supplier_train_from_company          = RelationshipFrom('.company.Company', 'SUPPLIES_TRAIN')
    supplier_valid_from_company          = RelationshipFrom('.company.Company', 'SUPPLIES_VALID')

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
    supplier_test_from_supplier           = RelationshipFrom('.supplier.Supplier', 'SUPPLIES_TEST')
    supplier_train_from_supplier          = RelationshipFrom('.supplier.Supplier', 'SUPPLIES_TRAIN')
    supplier_valid_from_supplier          = RelationshipFrom('.supplier.Supplier', 'SUPPLIES_VALID')


    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Suppplier',
                'nodes_related': self.serialize_relationships(self.supplier.all()),
            },
            {
                'nodes_type': 'Parent',
                'nodes_related': self.serialize_relationships(self.parent_to_company.all()),
            },
            {
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.partner_from_company.all()),
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
