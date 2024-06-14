from django import template
from ..models import *

register = template.Library()

@register.filter(name='is_subscribed')
def is_subscribed(user, vendor_id):
    return Subscription.is_subscribed(user, vendor_id)

@register.filter(name='was_subscribed')
def was_subscribed(user, vendor_id):
    return Subscription.was_subscribed(user, vendor_id)