# Generated by Django 5.0.4 on 2024-04-09 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cargos", "0009_alter_cargo_number_nf_alter_cargo_pallets_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cargo",
            name="number_nf",
            field=models.IntegerField(verbose_name="Número da Nota Fiscal"),
        ),
    ]
