# Generated by Django 3.1.1 on 2020-09-23 07:11

import appsapp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=128)),
                ('position', models.CharField(max_length=128)),
                ('result', models.BooleanField(default=True)),
                ('process_start_date', models.DateField()),
                ('process_end_date', models.DateField(null=True)),
                ('next_step', models.CharField(max_length=256)),
                ('status', models.IntegerField(choices=[(0, 'Application Sent'), (1, 'Interview Scheduled'), (2, "Waiting for an Answer from the Company's Side"), (3, "Waiting for an Answer from the Candidate's Side"), (4, 'Application Inactive - Rejected'), (5, 'Application Completed - Accepted'), (6, 'Hired')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=appsapp.models.make_path)),
                ('file_type', models.IntegerField(choices=[(0, 'CV'), (1, 'Cover Letter'), (2, 'Transcript of Records'), (3, 'Ranking Confirmation'), (4, 'Other')])),
                ('file_name', models.CharField(max_length=256)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appsapp.jobapplication')),
            ],
        ),
    ]