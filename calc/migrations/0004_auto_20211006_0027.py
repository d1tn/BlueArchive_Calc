# Generated by Django 3.2.6 on 2021-10-05 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0003_rename_host_inputdata_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdata',
            name='host',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='inputdata',
            name='ip',
            field=models.CharField(default='', max_length=64),
        ),
    ]
