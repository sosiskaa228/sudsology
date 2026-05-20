from django.db import migrations, models


def clear_orders(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(clear_orders, migrations.RunPython.noop),
        migrations.AddField(
            model_name="order",
            name="number",
            field=models.PositiveIntegerField(unique=True, serialize=False),
        ),
    ]
