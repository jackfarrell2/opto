from django.shortcuts import render
from csv import DictReader
from .models import Game, Player, Team, Slate, Position
from django.http import HttpResponseRedirect
from django.urls import reverse
from codecs import iterdecode
from datetime import datetime
from backports.zoneinfo import ZoneInfo
from fuzzywuzzy import fuzz


def update_slates(request):
    """Administrator route for updating active slates"""
    # Show active slates
    all_slates = Slate.objects.all().order_by('date')
    context = {"slates": all_slates}
    return render(request, 'nfl/update_slates.html', context=context)


def delete_slate(request, slate):
    """Delete a slate from the database"""
    slate = Slate.objects.get(pk=slate)
    slate.delete()
    return HttpResponseRedirect(reverse('update_slates'))


def add_slate(request):
    # Get uploaded csv file
    slate_file = request.FILES['slate-csv']
    csv = DictReader(iterdecode(slate_file, 'utf-8'))
    # Gather slates game info
    game_times = []
    teams = []
    games = []
    for row in csv:
        # Populate game times, teams, and games
        game_info = row['Game Info']
        if game_info == '-':
            # Pass players with no games
            continue
        if game_info not in games:
            games.append(game_info)  # Add game
        game_teams, game_time = game_info.split(" ", 1)
        away_team, home_team = game_teams.split('@')
        # Add teams
        if away_team not in teams:
            teams.append(away_team)
        if home_team not in teams:
            teams.append(home_team)
        # Add game times
        if game_time not in game_times:
            game_times.append(game_time)
    game_count = int(len(teams) / 2)  # Game Count
    # Store slate time
    earliest_game = sorted(game_times)[0]
    earliest_game = earliest_game[:-3]  # Strip time zone
    earliest_game = datetime.strptime(earliest_game, '%m/%d/%Y %I:%M%p')
    EDT = ZoneInfo('US/Eastern')  # Avoid naive datetime
    earliest_game = earliest_game.replace(tzinfo=EDT)
    # Create slate
    slate = Slate(date=earliest_game, game_count=game_count)
    slate.save()
    # Create teams for the slate
    for team in teams:
        # Add teams
        this_team = Team.objects.create(abbrev=team, slate=slate)
        this_team.save()
    for game in games:
        # Add games
        teams, time = game.split(' ', 1)
        # Add home and away teams
        away_team, home_team = teams.split('@')
        home_team = Team.objects.get(abbrev=home_team, slate=slate)
        away_team = Team.objects.get(abbrev=away_team, slate=slate)
        # Add game time
        time = time[:-3]
        time = datetime.strptime(time, '%m/%d/%Y %I:%M%p')
        time = earliest_game.replace(tzinfo=EDT)  # Avoid naive datetime
        this_game = Game.objects.create(time=time, home_team=home_team,
                                        away_team=away_team, slate=slate)
        this_game.save()
    # Save players and positions
    csv = DictReader(iterdecode(slate_file, 'utf-8'))
    for row in csv:
        position = Position.objects.get_or_create(position=row['Position'],
                                                  slate=slate)[0]
        team = Team.objects.get(abbrev=row['TeamAbbrev'], slate=slate)
        position = Position.objects.get(position=row['Position'], slate=slate)
        # Add player
        player = Player(name=row['Name'],
                        projection=0,
                        team=team,
                        position=position,
                        dk_id=row['ID'],
                        salary=row['Salary'],
                        slate=slate)
        player.save()
    return HttpResponseRedirect(reverse('update_slates'))


def update_default_projections(request, slate):
    # Accept csv
    projection_file = request.FILES['default-projections-csv']
    csv = DictReader(iterdecode(projection_file, 'utf-8'))
    this_slate = Slate.objects.get(pk=slate)  # Set slate
    # Pattern match names that don't match
    all_players = Player.objects.filter(slate=this_slate)
    for row in csv:
        player_name = row['Player']
        try:
            # Check if there is a perfect match
            player = Player.objects.get(name=player_name, slate=this_slate)
        except:
            # Check if there is a sudo-match
            for each_player in all_players:
                # Check un-altered names
                ratio = fuzz.ratio(each_player.name, player_name)
                if ratio > 85:
                    # Store sudo match
                    player = each_player
                    player.projection = row['FFPts']
                    player.save()
                    break
                # Check altered names
                # Alter first name
                stripped_db_name = ""
                for ch in each_player.name:
                    if ch.isalpha():
                        stripped_db_name += ch
                # Alter second name
                stripped_csv_name = ""
                for ch in player_name:
                    if ch.isalpha():
                        stripped_csv_name += ch
                ratio = fuzz.ratio(stripped_db_name, stripped_csv_name)
                partial_ratio = fuzz.partial_ratio(stripped_db_name,
                                                   stripped_csv_name)
                # Store sudo match
                if ratio > 75 and partial_ratio > 85:
                    player = each_player
                    player.projection = row['FFPts']
                    player.save()
                    break
            continue
        # Store perfect match
        player.projection = row['FFPts']
        player.save()
    return HttpResponseRedirect(reverse('update_slates'))


def index(request):
    all_slates = Slate.objects.all().order_by('date')
    slate = all_slates[0]
    players = Player.objects.filter(slate=slate)
    context = {'players': players}
    return render(request, 'nfl/index.html', context)
