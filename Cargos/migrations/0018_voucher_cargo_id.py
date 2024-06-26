# Generated by Django 5.0.4 on 2024-04-13 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "cargos",
            "0017_alter_cargo_shipment_date_alter_cargo_unloading_date_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="voucher",
            name="cargo_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vouchers",
                to="cargos.cargo",
                verbose_name="CARREGAMENTO",
            ),
            preserve_default=False,
        ),
    ]
