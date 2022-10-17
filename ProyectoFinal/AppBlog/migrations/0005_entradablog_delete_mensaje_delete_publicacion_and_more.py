# Generated by Django 4.1 on 2022-10-09 18:02

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppBlog', '0004_rename_perfilusuario_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=80)),
                ('subtitulo', models.CharField(max_length=100)),
                ('cuerpo', ckeditor.fields.RichTextField()),
                ('imagen', models.ImageField(upload_to='posteos')),
                ('fecha', models.DateTimeField()),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppBlog.categoria')),
            ],
        ),
        migrations.DeleteModel(
            name='Mensaje',
        ),
        migrations.DeleteModel(
            name='Publicacion',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatares/avatardefault.png', null=True, upload_to='avatares'),
        ),
    ]