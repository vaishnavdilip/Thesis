from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin

from .models import Company
from .models import Continent
from .models import Country
from .models import Industry
from .models import Sector

#  from .address import Address
#  from .intermediary import Intermediary
#  from .officer import Officer
#  from .other import Other

class CompanyAdmin(dj_admin.ModelAdmin):
    list_display = ("name",)
neo_admin.register(Company, CompanyAdmin)


