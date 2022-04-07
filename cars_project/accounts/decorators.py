from django.http import HttpResponse


# It will check if user is a part of any of the groups
# to check if he is a part of all the groups
# result should be checked with the groups. "if result == groups
def any_groups_required(groups=[]):
    def decorator(fun):
        def wrapper(request, *args, **kwargs):
            group = None
            user = request.user

            if user.is_superuser:
                return fun(request, *args, **kwargs)


            if not user.is_authenticated:
                return HttpResponse("You must be logged in!")

            if not user.groups.exists():
                return HttpResponse(f"You must be a part of one of the groups! {', '.join(groups)}")

            # Check if a group of the user is matching with the groups
            result = set(user.groups.all()).intersection(groups)

            if groups and not result:
                return HttpResponse(f"You must be a part of one of the groups! {', '.join(groups)}")
            return fun(request, *args, **kwargs)
        return wrapper
    return decorator