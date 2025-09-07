from __future__ import annotations
from django.db import models

class Deck(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    term = models.CharField(max_length=128)
    translation = models.CharField(max_length=128)
    example = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        unique_together = ('deck', 'term')
        ordering = ['term']

    def __str__(self) -> str:
        return f"{self.term} → {self.translation}"

class Attempt(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()
