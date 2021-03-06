# Generated by Django 2.0 on 2019-07-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_id', models.IntegerField()),
                ('citezen_id', models.IntegerField()),
                ('town', models.CharField(max_length=200)),
                ('street', models.CharField(max_length=200)),
                ('building', models.CharField(max_length=50)),
                ('appartment', models.IntegerField()),
                ('name', models.CharField(max_length=1000)),
                ('birth_day', models.DateField()),
                ('gender', models.CharField(max_length=6)),
                ('relatives', models.CharField(max_length=1000)),
            ],
        ),
    ]
