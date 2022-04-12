from profiles.models import Profile
from django import template
from django.template.context_processors import request

register = template.Library()

@register.inclusion_tag("profiles/is_complete.html", takes_context=True)
def is_complete(context): # Check if the profile of the user is all completed
    user_id = context.request.user.id # Current logged user
    profile = Profile.objects.get(pk=user_id) # Profile of the current logged user

    return {
        "is_complete": profile.is_complete,
    }







