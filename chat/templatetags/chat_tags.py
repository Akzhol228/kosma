from django.db.models import Count
from django import template
from ..models import Message

register = template.Library()


@register.simple_tag
def get_count_unread_message(user, object_id):
    return Message.objects.filter(
        object_id=object_id, is_read=False).exclude(from_user=user).count()


@register.simple_tag
def get_count_unread_demand_message(user, objects):
    return Message.objects.filter(
        object_id__in=objects, is_read=False).exclude(from_user=user).count()


@register.simple_tag
def get_merge_url(param1, param2):
    return str(param1) + '_' + str(param2)

