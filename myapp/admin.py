from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BookType, Book, Image , Commande


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(BookType)
admin.site.register(Book)
admin.site.register(Image)
admin.site.register(Commande)

