from django.contrib import admin
from .models import Demand, DemandDistribution, DemandFile

admin.site.register(Demand)
admin.site.register(DemandDistribution)
admin.site.register(DemandFile)
