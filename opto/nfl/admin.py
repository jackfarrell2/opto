from django.contrib import admin
from .models import Game, Player, Team, Slate, Position


admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Slate)
admin.site.register(Position)
