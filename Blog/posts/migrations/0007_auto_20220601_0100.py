# Generated by Django 3.2.8 on 2022-05-31 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_postviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='view_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.DeleteModel(
            name='PostViews',
        ),
    ]