import django_filters
from django_filters import DateRangeFilter,DateFilter
from task_management.models import Demand

class DemandFilter(django_filters.FilterSet):
    comment = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Demand
        fields = ['comment']

