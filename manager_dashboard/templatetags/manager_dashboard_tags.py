from django import template
from accounts.models import CustomUser

register = template.Library()

@register.simple_tag
def get_user_role_list(role):
    if role==1:
        return CustomUser.objects.filter(role=role).order_by("-id")
    if role==2:
        return CustomUser.objects.filter(role=role)