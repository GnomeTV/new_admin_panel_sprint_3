# Generated by Django 3.2 on 2022-09-28 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20220919_0921'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['rating'], name='film_work_rating_idx'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('genre', 'film_work'), name='genre_film_work_idx'),
        ),
        migrations.AddConstraint(
            model_name='personfilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'person', 'role'), name='film_work_person_idx'),
        ),
    ]
