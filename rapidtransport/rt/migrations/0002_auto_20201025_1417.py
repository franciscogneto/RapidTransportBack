# Generated by Django 3.1.2 on 2020-10-25 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('data_admissao', models.DateField()),
                ('data_aniversario', models.DateField()),
                ('tipo_carteira', models.CharField(choices=[('A', 'MOTO'), ('B', 'CARRO'), ('C', 'CAMINHÃO'), ('D', 'ONIBUS'), ('E', 'CARRETA')], max_length=1)),
                ('celular', models.CharField(max_length=18)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rt.empresa')),
            ],
        ),
    ]
