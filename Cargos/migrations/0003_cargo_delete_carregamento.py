# Generated by Django 5.0.4 on 2024-04-08 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Cargos", "0002_alter_carregamento_data_carregamento"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cargo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shipment_date", models.DateTimeField()),
                ("unloading_date", models.DateTimeField(blank=True)),
                ("pallets_quantity", models.IntegerField()),
                ("origin_company", models.CharField(max_length=50)),
                ("destination_company", models.CharField(max_length=50)),
                ("number_nf", models.CharField(max_length=50)),
                ("driver", models.CharField(max_length=50)),
                ("sale_or_disposal", models.BooleanField(blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Carregamento",
        ),
    ]
