# Generated by Django 2.0 on 2019-08-14 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imports',
            old_name='appartment',
            new_name='apartment',
        ),
        migrations.RenameField(
            model_name='imports',
            old_name='birth_day',
            new_name='birth_date',
        ),
        migrations.RenameField(
            model_name='imports',
            old_name='citezen_id',
            new_name='citizen_id',
        ),
    ]
