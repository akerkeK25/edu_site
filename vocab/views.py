from __future__ import annotations
from random import choice
from typing import Any
from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CardForm, CSVUploadForm, DeckForm
from .models import Card, Deck, Attempt

def deck_list(request: HttpRequest) -> HttpResponse:
    decks = Deck.objects.all().prefetch_related('cards')
    return render(request, 'vocab/deck_list.html', {'decks': decks, 'deck_form': DeckForm()})

def card_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Карточка добавлена!')
            return redirect('vocab:deck_list')
    else:
        form = CardForm()
    return render(request, 'vocab/card_create.html', {'form': form})

def upload_csv(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            created = 0
            with transaction.atomic():
                for row in rows:
                    deck_name = (row.get('deck') or 'Default').strip() or 'Default'
                    deck, _ = Deck.objects.get_or_create(name=deck_name)
                    term = row.get('term', '').strip()
                    translation = row.get('translation', '').strip()
                    example = (row.get('example') or '').strip()
                    image_url = (row.get('image_url') or '').strip()
                    Card.objects.get_or_create(
                        deck=deck, term=term,
                        defaults={'translation': translation, 'example': example, 'image_url': image_url}
                    )
                    created += 1
            messages.success(request, f'Загружено {created} карточек.')
            return redirect('vocab:deck_list')
    else:
        form = CSVUploadForm()
    return render(request, 'vocab/upload_csv.html', {'form': form})

def study(request: HttpRequest, deck_id: int) -> HttpResponse:
    deck = get_object_or_404(Deck, pk=deck_id)
    cards = list(deck.cards.all())
    if not cards:
        messages.warning(request, 'В колоде нет карточек.')
        return redirect('vocab:deck_list')
    card = choice(cards)
    request.session['current_card_id'] = card.id
    return render(request, 'vocab/study.html', {'deck': deck, 'card': card})

def _normalize(text: str) -> str:
    return ' '.join(text.strip().lower().split())

def check_answer(request: HttpRequest, deck_id: int) -> HttpResponse:
    if request.method != 'POST':
        return redirect('vocab:study', deck_id=deck_id)
    deck = get_object_or_404(Deck, pk=deck_id)
    card_id = request.session.get('current_card_id')
    card = get_object_or_404(Card, pk=card_id)
    user_answer = _normalize(request.POST.get('answer', ''))
    correct = _normalize(card.translation)
    is_ok = user_answer == correct
    Attempt.objects.create(card=card, is_correct=is_ok)
    context: dict[str, Any] = {'deck': deck, 'card': card, 'is_ok': is_ok, 'user_answer': user_answer}
    return render(request, 'vocab/study_result.html', context)
