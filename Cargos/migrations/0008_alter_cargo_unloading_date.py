# Generated by Django 5.0.4 on 2024-04-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cargos", "0007_alter_cargo_destination_company_alter_cargo_driver_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cargo",
            name="unloading_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Data de Recebimento"
            ),
        ),
    ]
