# Generated by Django 4.1 on 2022-09-06 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('game_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbrev', models.CharField(max_length=5)),
                ('slate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nfl.slate')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=5)),
                ('slate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nfl.slate')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('projection', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('dk_id', models.IntegerField()),
                ('salary', models.IntegerField()),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions_players', to='nfl.position')),
                ('slate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nfl.slate')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teams_players', to='nfl.team')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('away_team', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='away_game', to='nfl.team')),
                ('home_team', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='home_game', to='nfl.team')),
                ('slate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nfl.slate')),
            ],
        ),
    ]
