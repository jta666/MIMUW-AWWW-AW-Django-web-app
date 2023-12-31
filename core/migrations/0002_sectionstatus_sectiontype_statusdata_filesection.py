# Generated by Django 4.2.1 on 2023-05-10 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('compiles_with_warnings', 'Compiles with warnings'), ('compiles_without_warnings', 'Compiles without warnings'), ('does_not_compile', 'Does not compile')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('procedure', 'Procedure'), ('comment', 'Comment'), ('compiler_directives', 'Compiler Directives'), ('variable_declarations', 'Variable Declarations'), ('assembly_insert', 'Assembly Insert')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StatusData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(choices=[('compilation_error', 'Compilation error'), ('line_number_with_warning', 'Line number with warning')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FileSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('section_start', models.IntegerField()),
                ('section_end', models.IntegerField()),
                ('content', models.TextField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.file')),
                ('main_section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.filesection')),
                ('section_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sectionstatus')),
                ('section_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sectiontype')),
                ('status_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.statusdata')),
            ],
        ),
    ]
