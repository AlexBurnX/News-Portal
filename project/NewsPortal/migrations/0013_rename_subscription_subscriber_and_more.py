# Generated by Django 4.1.7 on 2023-03-16 07:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NewsPortal', '0012_alter_subscription_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscription',
            new_name='Subscriber',
        ),
        migrations.AlterModelOptions(
            name='subscriber',
            options={},
        ),
    ]
