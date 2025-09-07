from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=128)),
                ('translation', models.CharField(max_length=128)),
                ('example', models.CharField(blank=True, max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='vocab.deck')),
            ],
            options={'ordering': ['term'], 'unique_together': {('deck', 'term')}},
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_correct', models.BooleanField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.card')),
            ],
        ),
    ]
