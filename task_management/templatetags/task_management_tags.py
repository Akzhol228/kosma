from django.db.models import Count
from django import template
from ..models import DemandDistribution

register = template.Library()


@register.simple_tag
def get_selected_demand_distribution(query, status):
    return DemandDistribution.objects.filter(demand=query, status=status).first()



