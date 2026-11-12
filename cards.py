"""Vector playing-card artwork rendered as SVG.

Every card face (pips, aces and illustrated court cards) and the card back is
drawn here in code, so the app needs no image files or network access.
Images are returned as ``data:`` URIs that can be dropped into an ``<img>`` tag.
"""

from base64 import b64encode
from functools import lru_cache

W, H = 250, 350
CX, CY = W / 2, H / 2

RED = "#c8102e"
BLACK = "#1b1b1f"
GOLD = "#d4a72c"
GOLD_DARK = "#9a7414"
SKIN = "#f4d7b8"
INK = "#2a2118"

RANK_LABELS = {11: "J", 12: "Q", 13: "K", 14: "A"}

SUIT_PATHS = {
    "Hearts": (
        "M50 92 C22 68 0 48 0 28 C0 12 12 0 27 0 C38 0 46 7 50 17 "
        "C54 7 62 0 73 0 C88 0 100 12 100 28 C100 48 78 68 50 92 Z"
    ),
    "Diamonds": "M50 0 C62 18 74 34 88 50 C74 66 62 82 50 100 C38 82 26 66 12 50 C26 34 38 18 50 0 Z",
    "Spades": (
        "M50 0 C36 22 0 38 0 62 C0 78 12 88 27 88 C37 88 44 84 47 78 "
        "C46 88 42 95 32 100 L68 100 C58 95 54 88 53 78 C56 84 63 88 73 88 "
        "C88 88 100 78 100 62 C100 38 64 22 50 0 Z"
    ),
    "Clubs": (
        "M50 4 A22 22 0 0 1 68 39 A22 22 0 1 1 55 72 C56 84 60 93 70 100 "
        "L30 100 C40 93 44 84 45 72 A22 22 0 1 1 32 39 A22 22 0 0 1 50 4 Z"
    ),
}

CARD_BACKS = {
    "Crimson": ("#8e1b26", "#b3263a", "#f1d48a"),
    "Royal Blue": ("#13306b", "#1f4e9c", "#f1d48a"),
    "Emerald": ("#0c4a32", "#15704b", "#f1d48a"),
    "Onyx": ("#16161b", "#2c2c35", "#d4a72c"),
}


def suit_color(suit: str) -> str:
    return RED if suit in ("Hearts", "Diamonds") else BLACK


def _suit(suit: str, x: float, y: float, size: float, flip: bool = False, color: str | None = None) -> str:
    """Place a suit symbol centred at (x, y) with the given width."""
    fill = color or suit_color(suit)
    scale = size / 100
    rotate = f" rotate(180 {x} {y})" if flip else ""
    return (
        f'<g transform="{rotate.strip()}">'
        f'<path transform="translate({x - size / 2} {y - size / 2}) scale({scale})" '
        f'd="{SUIT_PATHS[suit]}" fill="{fill}"/></g>'
    )


def _corner_index(rank: int, suit: str) -> str:
    label = RANK_LABELS.get(rank, str(rank))
    color = suit_color(suit)
    spacing = ' letter-spacing="-3"' if label == "10" else ""
    one = (
        f'<text x="26" y="46" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" '
        f'font-size="36" font-weight="700" fill="{color}"{spacing}>{label}</text>'
        + _suit(suit, 26, 68, 22)
    )
    return one + f'<g transform="rotate(180 {CX} {CY})">{one}</g>'


# Pip coordinates for the number cards.
_L, _C, _R = 78, 125, 172
_ROWS4 = (82, 145, 205, 268)
PIP_LAYOUTS = {
    2: [(_C, 82), (_C, 268)],
    3: [(_C, 82), (_C, 175), (_C, 268)],
    4: [(_L, 82), (_R, 82), (_L, 268), (_R, 268)],
    5: [(_L, 82), (_R, 82), (_C, 175), (_L, 268), (_R, 268)],
    6: [(x, y) for y in (82, 175, 268) for x in (_L, _R)],
    7: [(x, y) for y in (82, 175, 268) for x in (_L, _R)] + [(_C, 128)],
    8: [(x, y) for y in (82, 175, 268) for x in (_L, _R)] + [(_C, 128), (_C, 222)],
    9: [(x, y) for y in _ROWS4 for x in (_L, _R)] + [(_C, 175)],
    10: [(x, y) for y in _ROWS4 for x in (_L, _R)] + [(_C, 113), (_C, 237)],
}


def _pips(rank: int, suit: str) -> str:
    size = 44 if rank < 9 else 40
    return "".join(_suit(suit, x, y, size, flip=y > CY) for x, y in PIP_LAYOUTS[rank])


def _ace(suit: str) -> str:
    if suit == "Spades":
        return (
            f'<circle cx="{CX}" cy="{CY}" r="70" fill="none" stroke="{GOLD}" stroke-width="2"/>'
            f'<circle cx="{CX}" cy="{CY}" r="64" fill="none" stroke="{GOLD}" stroke-width="0.8" stroke-dasharray="3 4"/>'
            + _suit(suit, CX, CY, 104)
            + f'<text x="{CX}" y="{CY + 92}" text-anchor="middle" font-family="Georgia, serif" '
            f'font-size="11" letter-spacing="4" fill="{GOLD_DARK}">WAR · ROYALE</text>'
        )
    return _suit(suit, CX, CY, 96)


def _court(rank: int, suit: str) -> str:
    """Draw a mirrored court card (Jack, Queen or King)."""
    red_suit = suit in ("Hearts", "Diamonds")
    robe = "#b3182f" if red_suit else "#1d3d7a"
    accent = "#1d3d7a" if red_suit else "#b3182f"
    hair = {11: "#6b3d1e", 12: "#e0b04a", 13: "#e8e2d6"}[rank]

    fx, fy, fw, fh = 50, 40, 150, 270
    defs = (
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#fff8e6"/><stop offset="1" stop-color="#f3e3bb"/></linearGradient>'
        f'<clipPath id="frame"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="6"/></clipPath>'
        "</defs>"
    )

    # Headwear differs by rank.
    if rank == 13:
        headwear = (
            f'<path d="M100 92 L100 66 L110 78 L118 60 L125 76 L132 60 L140 78 L150 66 L150 92 Z" '
            f'fill="{GOLD}" stroke="{GOLD_DARK}" stroke-width="1.5"/>'
            f'<rect x="99" y="88" width="52" height="7" fill="{GOLD_DARK}"/>'
            f'<circle cx="125" cy="84" r="3.5" fill="{accent}"/>'
            f'<circle cx="110" cy="86" r="2.5" fill="#2f9e6a"/><circle cx="140" cy="86" r="2.5" fill="#2f9e6a"/>'
        )
        held = (
            # Sword with hilt.
            f'<rect x="70" y="58" width="6" height="110" fill="#c9ced6" stroke="#6b717a" stroke-width="1"/>'
            f'<path d="M70 58 L73 48 L76 58 Z" fill="#c9ced6" stroke="#6b717a" stroke-width="1"/>'
            f'<rect x="62" y="150" width="22" height="5" rx="2" fill="{GOLD}" stroke="{GOLD_DARK}"/>'
        )
        face_hair = (
            f'<path d="M104 112 C104 140 116 150 125 150 C134 150 146 140 146 112 '
            f'C140 124 132 128 125 128 C118 128 110 124 104 112 Z" fill="{hair}" stroke="#9b958a" stroke-width="1"/>'
            f'<path d="M115 126 C120 122 130 122 135 126" fill="none" stroke="#9b958a" stroke-width="2.5"/>'
        )
    elif rank == 12:
        headwear = (
            f'<path d="M103 92 C106 80 112 74 115 70 C118 78 121 72 125 64 C129 72 132 78 135 70 '
            f'C138 74 144 80 147 92 Z" fill="{GOLD}" stroke="{GOLD_DARK}" stroke-width="1.5"/>'
            f'<circle cx="115" cy="70" r="3" fill="{GOLD}"/><circle cx="125" cy="63" r="3.5" fill="{accent}"/>'
            f'<circle cx="135" cy="70" r="3" fill="{GOLD}"/>'
        )
        held = (
            # A rose on a stem.
            f'<path d="M76 168 C74 140 78 118 80 100" fill="none" stroke="#2f7d4a" stroke-width="3"/>'
            f'<path d="M78 128 C68 124 66 116 70 112 C76 116 79 122 78 128 Z" fill="#2f9e6a"/>'
            f'<circle cx="80" cy="96" r="9" fill="{RED}" stroke="#8a0b1f" stroke-width="1"/>'
            f'<path d="M75 95 C79 90 85 92 84 98" fill="none" stroke="#8a0b1f" stroke-width="1.2"/>'
        )
        face_hair = (
            f'<path d="M102 102 C96 130 98 150 104 160 L112 140 C108 126 108 112 110 102 Z" fill="{hair}"/>'
            f'<path d="M148 102 C154 130 152 150 146 160 L138 140 C142 126 142 112 140 102 Z" fill="{hair}"/>'
        )
    else:
        headwear = (
            f'<path d="M100 98 C98 78 112 70 126 70 C142 70 152 80 150 98 Z" fill="{accent}" '
            f'stroke="{INK}" stroke-width="1"/>'
            f'<rect x="99" y="94" width="52" height="6" rx="2" fill="{GOLD}"/>'
            f'<path d="M146 80 C160 66 170 62 178 64 C168 70 160 78 150 88 Z" fill="{GOLD}" stroke="{GOLD_DARK}"/>'
        )
        held = (
            # A halberd.
            f'<rect x="72" y="62" width="4" height="108" fill="#8a5a2b"/>'
            f'<path d="M76 70 C92 72 96 84 94 96 C88 88 82 86 76 86 Z" fill="#c9ced6" stroke="#6b717a"/>'
            f'<path d="M72 74 L64 80 L72 84 Z" fill="#c9ced6" stroke="#6b717a"/>'
            f'<path d="M74 52 L78 64 L70 64 Z" fill="#c9ced6" stroke="#6b717a"/>'
        )
        face_hair = (
            f'<path d="M103 104 C102 118 104 126 108 130 L110 108 Z" fill="{hair}"/>'
            f'<path d="M147 104 C148 118 146 126 142 130 L140 108 Z" fill="{hair}"/>'
        )

    half = (
        # Robe and trims.
        f'<path d="M58 175 C60 150 82 138 104 135 L146 135 C168 138 190 150 192 175 Z" fill="{robe}"/>'
        f'<path d="M58 175 C60 150 82 138 104 135 L146 135 C168 138 190 150 192 175" fill="none" '
        f'stroke="{GOLD}" stroke-width="3"/>'
        f'<path d="M112 136 L112 175 M138 136 L138 175" stroke="{GOLD}" stroke-width="3"/>'
        f'<path d="M116 140 L134 140 L134 175 L116 175 Z" fill="{accent}"/>'
        + "".join(
            f'<circle cx="125" cy="{y}" r="2.4" fill="{GOLD}"/>' for y in (148, 158, 168)
        )
        + f'<path d="M104 135 L125 152 L146 135 L138 132 L125 142 L112 132 Z" fill="#fbf6ea" stroke="{INK}" stroke-width="0.8"/>'
        # Head.
        + f'<ellipse cx="125" cy="112" rx="21" ry="24" fill="{SKIN}" stroke="{INK}" stroke-width="1.2"/>'
        + f'<circle cx="117" cy="110" r="2.2" fill="{INK}"/><circle cx="133" cy="110" r="2.2" fill="{INK}"/>'
        + f'<path d="M113 104 L120 103 M130 103 L137 104" stroke="{INK}" stroke-width="1.5"/>'
        + f'<path d="M125 112 L122 120 L126 120" fill="none" stroke="{INK}" stroke-width="1"/>'
        + f'<path d="M119 127 C123 130 127 130 131 127" fill="none" stroke="#b0414b" stroke-width="1.8"/>'
        + face_hair
        + headwear
        + held
        + _suit(suit, 176, 116, 20)
    )

    letter = RANK_LABELS[rank]
    return (
        defs
        + f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="6" fill="url(#bg)"/>'
        + '<g clip-path="url(#frame)">'
        + half
        + f'<g transform="rotate(180 {CX} {CY})">{half}</g>'
        + f'<path d="M{fx} {CY} L{fx + fw} {CY}" stroke="{GOLD_DARK}" stroke-width="1.5"/>'
        + "</g>"
        + f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="6" fill="none" stroke="{GOLD_DARK}" stroke-width="2.5"/>'
        + f'<rect x="{fx + 4}" y="{fy + 4}" width="{fw - 8}" height="{fh - 8}" rx="4" fill="none" '
        f'stroke="{suit_color(suit)}" stroke-width="0.8" opacity="0.6"/>'
        + f'<text x="{fx + 14}" y="{fy + 26}" font-family="Georgia, serif" font-size="20" '
        f'font-weight="700" fill="{suit_color(suit)}" opacity="0.85">{letter}</text>'
    )


def _wrap(body: str) -> str:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
        f"{body}</svg>"
    )
    return "data:image/svg+xml;base64," + b64encode(svg.encode()).decode()


def _blank_face() -> str:
    return (
        f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16" fill="#fffdf8" stroke="#c9c2b3" stroke-width="2"/>'
    )


@lru_cache(maxsize=None)
def card_image(rank: int, suit: str) -> str:
    """Return a data URI for the face of a card."""
    if rank == 14:
        art = _ace(suit)
    elif rank >= 11:
        art = _court(rank, suit)
    else:
        art = _pips(rank, suit)
    return _wrap(_blank_face() + art + _corner_index(rank, suit))


@lru_cache(maxsize=None)
def card_back(style: str = "Crimson") -> str:
    """Return a data URI for a patterned card back."""
    dark, light, trim = CARD_BACKS.get(style, CARD_BACKS["Crimson"])
    body = (
        "<defs>"
        '<pattern id="lattice" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="18" height="18" fill="{dark}"/>'
        f'<rect x="0" y="0" width="9" height="9" fill="{light}"/>'
        f'<rect x="9" y="9" width="9" height="9" fill="{light}"/>'
        f'<circle cx="9" cy="9" r="1.6" fill="{trim}" opacity="0.7"/>'
        "</pattern>"
        "</defs>"
        f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16" fill="#fffdf8" stroke="#c9c2b3" stroke-width="2"/>'
        f'<rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="10" fill="url(#lattice)"/>'
        f'<rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="10" fill="none" stroke="{trim}" stroke-width="3"/>'
        f'<rect x="22" y="22" width="{W - 44}" height="{H - 44}" rx="7" fill="none" stroke="{trim}" stroke-width="1" opacity="0.7"/>'
        f'<ellipse cx="{CX}" cy="{CY}" rx="52" ry="66" fill="{dark}" stroke="{trim}" stroke-width="3"/>'
        f'<ellipse cx="{CX}" cy="{CY}" rx="44" ry="58" fill="none" stroke="{trim}" stroke-width="1"/>'
        + _suit("Spades", CX, CY - 18, 34, color=trim)
        + f'<text x="{CX}" y="{CY + 30}" text-anchor="middle" font-family="Georgia, serif" font-size="22" '
        f'font-weight="700" letter-spacing="5" fill="{trim}">WAR</text>'
    )
    return _wrap(body)
