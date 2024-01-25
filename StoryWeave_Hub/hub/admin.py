from django.contrib import admin

from .models import Branch, MainStory, Vote


admin.site.register(Branch)
admin.site.register(MainStory)
admin.site.register(Vote)
