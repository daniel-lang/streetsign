# Generated by Django 2.2 on 2019-09-14 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New Feed', max_length=100)),
                ('slug', models.SlugField(allow_unicode=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='draft', max_length=16)),
                ('contenttype', models.SlugField(allow_unicode=True, default='plaintext', max_length=100)),
                ('content_json', models.TextField(blank=True, default='{}')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_all', to='core.Feed')),
            ],
        ),
    ]
