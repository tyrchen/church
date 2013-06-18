from django.contrib import admin
from church.forms import TeamForm
from church.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'members', 'created', 'updated')
    form = TeamForm

admin.site.register(Team, TeamAdmin)