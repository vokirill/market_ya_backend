# Generated by Django 2.0 on 2019-07-22 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imports',
            old_name='citezen_id',
            new_name='citizen_id',
        ),
    ]
