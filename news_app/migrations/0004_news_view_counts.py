# Generated by Django 5.0.3 on 2024-04-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='view_counts',
            field=models.IntegerField(default=0),
        ),
    ]
