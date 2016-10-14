# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='filtered_image_file',
            field=models.ImageField(null=True, upload_to='static_files/uploaded'),
        ),
        migrations.AddField(
            model_name='photo',
            name='image_file',
            field=models.ImageField(null=True, upload_to='static_files/uploaded'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(max_length=500, blank=True),
        ),
    ]
