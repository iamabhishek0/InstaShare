# Generated by Django 2.1.5 on 2019-04-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20190222_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tagged_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]