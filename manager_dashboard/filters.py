import django_filters
from django_filters import DateRangeFilter,DateFilter
from task_management.models import Demand

class DemandFilter(django_filters.FilterSet):
    DIPLOM_TYPE_CHOICES = (
        (1, 'Общая'),
        (2, 'Теория'),
        (3, 'Практика')
    )
    comment = django_filters.CharFilter(lookup_expr='icontains')
    diplom_type = django_filters.ChoiceFilter(label='Тип Дип. Работы', 
        choices=DIPLOM_TYPE_CHOICES)
    student_email = django_filters.CharFilter(field_name='student__email', 
        lookup_expr='icontains')

    class Meta:
        model = Demand
        fields = ['comment', 'diplom_type']


