# Generated by Django 2.0 on 2019-07-31 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0003_auto_20190722_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imports',
            name='id',
        ),
        migrations.AlterField(
            model_name='imports',
            name='import_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]