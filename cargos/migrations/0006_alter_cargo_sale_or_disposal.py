# Generated by Django 5.0.4 on 2024-04-09 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cargos", "0005_alter_cargo_unloading_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cargo",
            name="sale_or_disposal",
            field=models.BooleanField(default=False),
        ),
    ]