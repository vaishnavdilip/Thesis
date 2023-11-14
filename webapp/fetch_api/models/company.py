from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty,
)

from neomodel.contrib.spatial_properties import NeomodelPoint

from django_neomodel import DjangoNode

from .nodeutils import NodeUtils


class Company(DjangoNode, NodeUtils):

    city_state_postal        = StringProperty()
    code                     = StringProperty()
    coefficientTest          = StringProperty()
    coefficientTrain         = StringProperty()
    coefficientValid         = StringProperty()
    id                       = UniqueIdProperty(primary_key = True) # Company ID
    location_street1         = StringProperty()
    nace_description         = StringProperty()
    name                     = UniqueIdProperty(primary_key = False) # Company name
    point                    = StringProperty()
    triangleTest             = StringProperty()
    triangleTrain            = StringProperty()
    triangleValid            = StringProperty()
    countries                  = StringProperty()
    industries                 = StringProperty()

    # Relationships
    supplier_to               = RelationshipTo('.company.Company', 'SUPPLIES')
    supplier_of               = RelationshipFrom('.company.Company', 'SUPPLIES')
    partner                 = Relationship('.company.Company', 'PARTNERS')
    competitor              = Relationship('.company.Company', 'COMPETES')
    parent_of                  = RelationshipTo('.company.Company', 'ULTIMATE_PARENT_OF')
    parent_from                = RelationshipFrom('.company.Company', 'ULTIMATE_PARENT_OF')


    supplier_test           = Relationship('.company.Company', 'SUPPLIES_TEST')
    supplier_train          = Relationship('.company.Company', 'SUPPLIES_TRAIN')
    supplier_valid          = Relationship('.company.Company', 'SUPPLIES_VALID')
    # Country Node

    country                 = RelationshipTo('.country.Country', 'IN_COUNTRY')
    
    # Industry Node

    industry                = RelationshipTo('.industry.Industry', 'IN_INDUSTRY')

    class Meta:
        app_label = "fetch_api"

    @property
    def serialize(self):
        return {
            'node_properties': {
                   'city_state_postal' : self.city_state_postal,
                   'code' : self.code,
                   'coefficientTest' : self.coefficientTest,
                   'coefficientTrain' : self.coefficientTrain,
                   'coefficientValid' : self.coefficientValid,
                   'id' : self.id,
                   'location_street1' : self.location_street1,
                   'nace_description' : self.nace_description,
                   'name' : self.name,
                   'point' : self.point,
                   'triangleTest' : self.triangleTest,
                   'triangleTrain' : self.triangleTrain,
                   'triangleValid' : self.triangleValid,
                   'countries' : self.countries,
                   'industries' : self.industries,           
            },
        }
    
    @property
    def serialize_connections(self):
        return [
            {   'name': 'Supplies to',
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.supplier_to.all()),
            },
            {   'name': 'Supplies from',
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.supplier_of.all()),
            },
            {   'name': 'Partners',
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.partner.all()),
            },
            {   'name': 'Competitors',
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.competitor.all()),
            },
            {   'name': 'Parent Of',
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.parent_of.all()),
            },
            {   'name': 'Parent to',
                'nodes_type': 'Company',
                'nodes_related': self.serialize_relationships(self.parent_from.all()),
            },
            {   'name': 'Country',
                'nodes_type': 'Country',
                'nodes_related': self.serialize_relationships(self.country.all()),
            },
            {   'name': 'Industry',
                'nodes_type': 'Industry',
                'nodes_related': self.serialize_relationships(self.industry.all())
            },
        ]
