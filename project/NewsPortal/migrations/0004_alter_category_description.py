# Generated by Django 4.1.7 on 2023-02-26 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPortal', '0003_alter_author_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
