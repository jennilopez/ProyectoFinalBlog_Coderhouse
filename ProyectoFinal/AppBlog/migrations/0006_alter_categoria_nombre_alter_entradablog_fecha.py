# Generated by Django 4.1 on 2022-10-17 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppBlog', '0005_entradablog_delete_mensaje_delete_publicacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='entradablog',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
