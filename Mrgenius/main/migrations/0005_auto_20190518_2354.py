# Generated by Django 2.2 on 2019-05-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190410_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='wiki_doc',
            field=models.TextField(blank=True, null=True, verbose_name='wiki_doc'),
        ),
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(max_length=20, verbose_name='password'),
        ),
    ]
