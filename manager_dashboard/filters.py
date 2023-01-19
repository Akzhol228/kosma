import django_filters
from django_filters import DateRangeFilter,DateFilter
from task_management.models import Demand
from main.models import CallBack

class DemandFilter(django_filters.FilterSet):
    comment = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Demand
        fields = ['comment']


class CallBackFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CallBack
        fields = ['first_name', 'phone_number']
