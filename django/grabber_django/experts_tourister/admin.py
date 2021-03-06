from django.contrib import admin
from experts_tourister.models import Profile
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('name', 'country', 'email', 'telephone','url_profile')
    list_display=('name', 'country', 'email', 'telephone','url_profile','status')
    list_per_page = 25

admin.site.register(Profile, ProfileAdmin)