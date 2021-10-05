# Generated by Django 3.2.6 on 2021-10-05 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdata',
            name='host',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='inputdata',
            name='authKeys',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
