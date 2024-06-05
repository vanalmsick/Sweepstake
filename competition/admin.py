# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Tournament, Group, Participant, Match


# Register your models here.
class GroupsInline(admin.TabularInline):
    """Table of Groups to show in Tournament detail view - 2nd highest level for grouping Tournament participants for group-phase"""

    model = Group
    fk_name = "tournament"
    extra = 0


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Admin view of Tournament - the highest level e.g. Football World Cup 2024"""

    list_display = [
        "name",
    ]
    inlines = [
        GroupsInline,
    ]


@admin.register(Participant)
class ParticipantsAdmin(admin.ModelAdmin):
    """Admin view of Tournament Participants e.g. countries like Germany, UK, France, etc."""

    list_display = [
        "name",
        "group",
    ]
    ordering = ("name",)


@admin.register(Match)
class MatchesAdmin(admin.ModelAdmin):
    """Admin view to view the scheduled Matches e.g. on Sunday at 6pm X plays against Y"""

    list_display = [
        "phase",
        "match_time",
        "team_a_placeholder",
        "team_b_placeholder",
    ]
    ordering = ("match_time",)
