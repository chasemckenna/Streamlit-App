"""Core rules for the two-player War card game."""

import random

Card = tuple[int, str]

RANK_NAMES = {
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace",
}
SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")


def create_deck() -> list[Card]:
    """Return a standard 52-card deck."""
    return [(rank, suit) for suit in SUITS for rank in range(2, 15)]


def new_game(player_name: str, round_limit: int) -> dict:
    """Create and shuffle a game, then deal 26 cards to each player."""
    deck = create_deck()
    random.shuffle(deck)
    return {
        "player_name": player_name.strip() or "You",
        "player_deck": deck[:26],
        "computer_deck": deck[26:],
        "round_limit": round_limit,
        "rounds": 0,
        "wars": 0,
        "history": [],
        "last_round": None,
        "status": "playing",
        "winner": None,
    }


def card_name(card: Card) -> str:
    """Format a card's rank and suit for display."""
    rank, suit = card
    return f"{RANK_NAMES.get(rank, str(rank))} of {suit}"


def _award_pot(winner_deck: list[Card], pot: list[Card]) -> None:
    winner_deck.extend(pot)


def play_round(game: dict) -> dict:
    """Play one round, resolving any tied cards as successive wars."""
    if game["status"] != "playing":
        return game

    player_deck = game["player_deck"]
    computer_deck = game["computer_deck"]
    if not player_deck or not computer_deck:
        _finish_by_cards(game)
        return game

    pot: list[Card] = []
    player_card = player_deck.pop(0)
    computer_card = computer_deck.pop(0)
    player_opening = player_card
    computer_opening = computer_card
    pot.extend((player_card, computer_card))
    war_cards: list[tuple[Card | None, Card | None]] = []
    war_count = 0

    while player_card[0] == computer_card[0]:
        war_count += 1
        game["wars"] += 1
        for _ in range(3):
            if player_deck:
                pot.append(player_deck.pop(0))
            if computer_deck:
                pot.append(computer_deck.pop(0))

        player_card = player_deck.pop(0) if player_deck else None
        computer_card = computer_deck.pop(0) if computer_deck else None
        if player_card:
            pot.append(player_card)
        if computer_card:
            pot.append(computer_card)
        war_cards.append((player_card, computer_card))

        if player_card is None or computer_card is None:
            break

    if player_card is None and computer_card is None:
        player_deck.extend(pot[::2])
        computer_deck.extend(pot[1::2])
        game["status"] = "finished"
        game["winner"] = "Tie"
        round_winner = "Draw"
    elif computer_card is None or (
        player_card is not None and player_card[0] > computer_card[0]
    ):
        _award_pot(player_deck, pot)
        round_winner = game["player_name"]
    else:
        _award_pot(computer_deck, pot)
        round_winner = "Computer"

    game["rounds"] += 1
    game["last_round"] = {
        "player_opening": player_opening,
        "computer_opening": computer_opening,
        "war_cards": war_cards,
        "war_count": war_count,
        "winner": round_winner,
        "cards_awarded": len(pot),
    }
    game["history"].append(game["last_round"])

    if game["status"] == "playing" and (not player_deck or not computer_deck):
        _finish_by_cards(game)
    elif game["status"] == "playing" and game["rounds"] >= game["round_limit"]:
        if len(player_deck) > len(computer_deck):
            game["winner"] = game["player_name"]
        elif len(computer_deck) > len(player_deck):
            game["winner"] = "Computer"
        else:
            game["winner"] = "Tie"
        game["status"] = "limit"

    return game


def _finish_by_cards(game: dict) -> None:
    player_count = len(game["player_deck"])
    computer_count = len(game["computer_deck"])
    if player_count > computer_count:
        game["winner"] = game["player_name"]
    elif computer_count > player_count:
        game["winner"] = "Computer"
    else:
        game["winner"] = "Tie"
    game["status"] = "finished"