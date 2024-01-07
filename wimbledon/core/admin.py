from django.contrib import admin

from .models import Tournament


class TournamentAdmin(admin.ModelAdmin):
    list_display = ("description", "done")


admin.site.register(Tournament, TournamentAdmin)
