from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Following


class FollowingInline(admin.TabularInline):
    model = Following
    fk_name = 'follower'
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (FollowingInline, )
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', )

    list_filter = ('email', 'username')
    search_fields = ('username', 'email')


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('follower', 'leader')

