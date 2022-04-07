from django.contrib import admin
from importlib._common import _
from accounts.models import CarsUser
from profiles.models import Profile

from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin

UserModel = get_user_model()



# Register your models here.
@admin.register(UserModel)
class CarsUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    ordering = ('email',)

    # Fieldsets are present in AbstractBaseUser inherited in the models
    # this lets us assign groups and permissions in the admin center to the users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        # Added date_joined from models.py to make it visible in admin panel
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Adding date_joined from models.py to be visible in admin panel
    # must add this line in order to not get an error message
    readonly_fields = ('date_joined',)
