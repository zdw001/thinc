# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Idea, Profile

# set up automated slug creation
class IdeaAdmin(admin.ModelAdmin):
	model = Idea
	list_display = ('user', 'name', 'overview', 'description', 'published_date', 'votes',)
	prepopulated_fields = {'slug': ('name',)}

class ProfileAdmin(admin.ModelAdmin):
	model = Profile
	list_display = ('user', 'photo', 'website', 'bio', 'phone', 'city', 'country')

# Register your models here.
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Profile, ProfileAdmin)