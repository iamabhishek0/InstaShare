# Generated by Django 2.1.5 on 2019-04-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_post_tagged_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tagging',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='want_to_tag',
            field=models.BooleanField(default=False),
        ),
    ]