# Generated by Django 2.2.1 on 2019-08-13 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')])),
                ('college', models.CharField(max_length=200)),
                ('phoneNum', models.CharField(max_length=11)),
                ('password', models.CharField(max_length=20)),
                ('enrollmentTime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searchTime', models.DateTimeField()),
                ('searchContent', models.CharField(max_length=2000)),
                ('isValid', models.BooleanField()),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusqa.User')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('questionId', models.AutoField(primary_key=True, serialize=False)),
                ('createTime', models.DateTimeField()),
                ('editTime', models.DateTimeField(null=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=2000)),
                ('createUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusqa.User')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('answerID', models.AutoField(primary_key=True, serialize=False)),
                ('createTime', models.DateTimeField()),
                ('editTime', models.DateTimeField(null=True)),
                ('content', models.CharField(max_length=2000)),
                ('createUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusqa.User')),
                ('questionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusqa.Questions')),
            ],
        ),
    ]
