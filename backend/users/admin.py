from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'last_name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
