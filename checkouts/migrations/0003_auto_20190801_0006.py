# Generated by Django 2.2.3 on 2019-08-01 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0002_auto_20190801_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='current_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkouts.Student'),
        ),
    ]
