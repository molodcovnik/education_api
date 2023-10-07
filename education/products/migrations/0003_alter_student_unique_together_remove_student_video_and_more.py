# Generated by Django 4.2.5 on 2023-10-05 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_alter_product_lessons'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('video', 'user')},
        ),
        migrations.RemoveField(
            model_name='student',
            name='video',
        ),
        migrations.AddField(
            model_name='student',
            name='video',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='views', to='products.video'),
        ),
    ]