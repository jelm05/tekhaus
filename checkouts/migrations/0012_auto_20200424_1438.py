# Generated by Django 2.2.7 on 2020-04-24 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0011_auto_20191112_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='primary_email',
            field=models.EmailField(default='temp_email@sva.edu', max_length=100, verbose_name='Primary Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='secondary_email',
            field=models.EmailField(blank=True, max_length=100, verbose_name='Secondary Email'),
        ),
    ]
