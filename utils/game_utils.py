import random
def shuffle_cards(cards):
    """Shuffle the list of cards."""
    random.shuffle(cards)
def check_match(cards, flipped_cards):
    """Check if the two flipped cards match."""
    return cards[flipped_cards[0]] == cards[flipped_cards[1]]