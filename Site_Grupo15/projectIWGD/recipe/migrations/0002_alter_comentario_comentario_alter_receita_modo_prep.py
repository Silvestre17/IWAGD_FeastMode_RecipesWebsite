# Generated by Django 4.1 on 2023-10-02 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comentario",
            name="comentario",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="receita",
            name="modo_prep",
            field=models.TextField(default=""),
        ),
    ]
