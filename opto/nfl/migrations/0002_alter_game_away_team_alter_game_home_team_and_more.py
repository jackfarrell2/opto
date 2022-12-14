# Generated by Django 4.1 on 2022-09-07 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='away_team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='away_game', to='nfl.team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='home_game', to='nfl.team'),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams_players', to='nfl.team'),
        ),
    ]
