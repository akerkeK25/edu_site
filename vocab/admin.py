from django.contrib import admin
from .models import Deck, Card, Attempt

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'deck', 'term', 'translation')
    list_filter = ('deck',)
    search_fields = ('term', 'translation')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'is_correct', 'created_at')
    list_filter = ('is_correct',)
