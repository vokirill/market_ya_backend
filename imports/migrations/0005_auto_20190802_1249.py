# Generated by Django 2.0 on 2019-08-02 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0004_auto_20190731_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imports',
            old_name='appartment',
            new_name='apartment',
        ),
    ]