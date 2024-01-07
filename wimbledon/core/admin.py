from django.contrib import admin

from .models import Tournament, Competitor, Match


class TournamentAdmin(admin.ModelAdmin):
    list_display = ("description", "done")


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Competitor)
admin.site.register(Match)
