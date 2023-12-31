# Generated by Django 4.2.3 on 2023-07-14 16:45

from django.db import migrations, models
import django.db.models.deletion
import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicadorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('dimensao', models.CharField(choices=[('O', 'Organização Didático-Pedagógica'), ('C', 'Corpo Docente e Tutorial'), ('I', 'Infraestrutura')], max_length=1)),
                ('mensagem_aviso', models.TextField(blank=True)),
                ('tabela_conceitos', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='IndicadorMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsa', models.BooleanField(default=False)),
                ('nivel_suposto', models.IntegerField(null=True)),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('conteudo', models.FileField(upload_to='relatorios/', validators=[validators.validate_pdf_file])),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('indicador_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicadores.indicadorinfo')),
            ],
        ),
    ]
