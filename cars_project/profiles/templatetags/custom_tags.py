from profiles.models import Profile
from django import template
from django.template.context_processors import request

register = template.Library()

@register.inclusion_tag("profiles/is_complete.html", takes_context=True)
def is_complete(context):
    user_id = context.request.user.id
    profile = Profile.objects.get(pk=user_id)

    return {
        "is_complete": profile.is_complete,
    }







