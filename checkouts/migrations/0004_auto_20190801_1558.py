# Generated by Django 2.2.3 on 2019-08-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0003_auto_20190801_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='past_checkouts',
            field=models.ManyToManyField(blank=True, null=True, related_name='past_checkouts', to='checkouts.Checkout'),
        ),
        migrations.AlterField(
            model_name='student',
            name='current_equipment',
            field=models.ManyToManyField(blank=True, null=True, related_name='current_equipment', to='checkouts.Equipment'),
        ),
        migrations.AlterField(
            model_name='student',
            name='past_equipment',
            field=models.ManyToManyField(blank=True, null=True, related_name='past_equipment', to='checkouts.Equipment'),
        ),
    ]
