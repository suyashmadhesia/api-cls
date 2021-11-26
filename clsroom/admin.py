from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from clsroom.accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from .models import *

User = get_user_model()

# Remove Group Model from admin.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['account_id', 'is_staff']
    list_filter = ['is_staff']
    
    fieldsets = (
        (None, {'fields': ('email','password',)}),
        ('Personal info', {'fields': ('name', 'branch',)}),
        ('Permissions', {'fields': ('is_staff', 'is_faculty', 'cls_room_id',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2', 'account_id')}
         ),
    )
    search_fields = ['account_id']
    ordering = ['account_id']
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  

        if not is_superuser:
            disabled_fields |= {
                'is_staff',
                'email',
                'password',
                'is_superuser',
                'is_faculty'
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'email',
                'password',
                'is_superuser',
                'is_faculty'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
    


admin.site.register(Classroom)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(MediaFile)
admin.site.register(User, UserAdmin)
