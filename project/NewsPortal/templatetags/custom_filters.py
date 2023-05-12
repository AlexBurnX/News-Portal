from django import template
from pytz import timezone

register = template.Library()


@register.filter(name='show_time')
def show_time(value, tz):
    t = value.astimezone(timezone(tz))
    h = t.time().strftime("%H")
    time = t.time().strftime("%H:%M")
    return (time)
