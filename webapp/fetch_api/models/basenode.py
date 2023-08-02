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


class Base(DjangoNode):

    city_state_postal        = StringProperty()
    code                     = StringProperty()
    coefficientTest          = StringProperty()
    coefficientTrain         = StringProperty()
    coefficientValid         = StringProperty()
    id                       = UniqueIdProperty(primary_key=True) # Company ID
    location_street1         = StringProperty()
    nace_description         = StringProperty()
    name                     = StringProperty() # Company name
    point                    = StringProperty()
    triangleTest             = StringProperty()
    triangleTrain            = StringProperty()
    triangleValid            = StringProperty()

    # Relationships
    supplier                = Relationship('.basenode.Base', 'SUPPLIES')
    partner                 = Relationship('.basenode.Base', 'PARTNERS')
    competitor              = Relationship('.basenode.Base', 'COMPETES')
    supplier_test           = Relationship('.basenode.Base', 'SUPPLIES_TEST')
    supplier_train          = Relationship('.basenode.Base', 'SUPPLIES_TRAIN')
    supplier_valid          = Relationship('.basenode.Base', 'SUPPLIES_VALID')

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
            },
        }
