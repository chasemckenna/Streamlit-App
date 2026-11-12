import streamlit as st

from cards import CARD_BACKS, card_back, card_image
from war_game import card_name, new_game, play_round

st.set_page_config(
    page_title="War Royale",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROUND_CHOICES = [25, 50, 100, 250, 500, 1000]

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --gold: #e3b84a;
  --gold-soft: rgba(227, 184, 74, 0.35);
  --cream: #f6efdc;
  --muted: rgba(246, 239, 220, 0.66);
  --panel: rgba(4, 28, 17, 0.55);
  --rival: #ef6f7f;
}

.stApp {
  background:
    radial-gradient(ellipse 80% 55% at 50% 30%, rgba(40, 150, 95, 0.55), transparent 70%),
    radial-gradient(ellipse at 50% 120%, #04170e 0%, transparent 60%),
    linear-gradient(180deg, #0e5233 0%, #0a3d26 55%, #062616 100%);
  background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 1.6rem; padding-bottom: 4rem; }
html, body, .stApp, .stMarkdown, p, label, input, button { font-family: 'Inter', system-ui, sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #07301d, #041a10); border-right: 1px solid var(--gold-soft); }

/* Buttons */
button[data-testid^="stBaseButton-primary"] {
  background: linear-gradient(180deg, #f3cf6b 0%, #d9a22c 100%) !important;
  color: #2b1d02 !important; border: 1px solid #f7dc8f !important;
  font-weight: 700 !important; letter-spacing: .04em; border-radius: 999px !important;
  box-shadow: 0 6px 18px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.5);
  transition: transform .12s ease, box-shadow .12s ease;
}
button[data-testid^="stBaseButton-primary"]:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(0,0,0,.45); }
button[data-testid^="stBaseButton-secondary"] {
  background: rgba(0,0,0,.25) !important; color: var(--cream) !important;
  border: 1px solid var(--gold-soft) !important; border-radius: 999px !important; font-weight: 600 !important;
}
button[data-testid^="stBaseButton-secondary"]:hover { border-color: var(--gold) !important; color: var(--gold) !important; }

/* Brand */
.brand { font-family: 'Cinzel', serif; font-weight: 800; letter-spacing: .18em; color: var(--gold);
  text-shadow: 0 2px 0 #5c4210, 0 10px 30px rgba(0,0,0,.5); margin: 0; line-height: 1; }
.brand-sm { font-size: 1.5rem; }
.eyebrow { font-size: .72rem; letter-spacing: .28em; text-transform: uppercase; color: var(--muted); }

/* Landing hero */
.hero { text-align: center; padding: 1.2rem 0 0.5rem; }
.hero .brand { font-size: clamp(2.8rem, 9vw, 5.4rem); }
.hero p.tag { color: var(--muted); font-size: 1.05rem; max-width: 560px; margin: .9rem auto 0; }
.fan { position: relative; height: 240px; margin: 1.4rem auto 3.2rem; width: 100%; max-width: 520px; }
.fan img { position: absolute; left: 50%; bottom: 0; width: 130px; margin-left: -65px; border-radius: 9px;
  transform-origin: 50% 120%; box-shadow: 0 14px 30px rgba(0,0,0,.5);
  animation: fanOut .9s cubic-bezier(.2,.8,.2,1) both; }
@keyframes fanOut { from { transform: rotate(0deg) translateY(30px); opacity: 0; } }

/* Scoreboard */
.scoreboard { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; align-items: center;
  background: var(--panel); border: 1px solid var(--gold-soft); border-radius: 18px; padding: 1rem 1.3rem;
  box-shadow: 0 18px 40px rgba(0,0,0,.35); backdrop-filter: blur(4px); }
.seat { display: flex; align-items: center; gap: 1rem; }
.seat.right { flex-direction: row-reverse; text-align: right; }
.seat .who { font-family: 'Cinzel', serif; font-size: 1.15rem; color: var(--cream); font-weight: 600; }
.seat .count { font-size: 2.1rem; font-weight: 700; color: var(--gold); line-height: 1.1; }
.seat.right .count { color: var(--rival); }
.seat .sub { font-size: .78rem; color: var(--muted); letter-spacing: .06em; }
.stack { position: relative; width: 58px; height: 82px; flex: none; }
.stack img { position: absolute; width: 54px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,.4); }
.stack .empty { position: absolute; inset: 0; border: 2px dashed var(--gold-soft); border-radius: 6px; }
.center-info { text-align: center; min-width: 190px; }
.center-info .round { font-family: 'Cinzel', serif; font-size: 1.35rem; color: var(--cream); }
.share { height: 10px; border-radius: 99px; overflow: hidden; display: flex; margin-top: .55rem;
  background: rgba(0,0,0,.35); box-shadow: inset 0 1px 2px rgba(0,0,0,.5); }
.share .p { background: linear-gradient(90deg, #b8861e, var(--gold)); transition: width .4s; }
.share .c { background: linear-gradient(90deg, #ef6f7f, #b83246); transition: width .4s; }

/* Table */
.table { margin-top: 1.2rem; border-radius: 28px; padding: 1.6rem 1rem 1.4rem;
  background: radial-gradient(ellipse at 50% 40%, rgba(255,255,255,.07), rgba(0,0,0,.12) 70%);
  border: 2px solid rgba(227,184,74,.25); box-shadow: inset 0 0 60px rgba(0,0,0,.35), 0 20px 50px rgba(0,0,0,.3); }
.duel { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: .5rem; }
.slot { text-align: center; }
.slot .label { font-size: .75rem; letter-spacing: .24em; text-transform: uppercase; color: var(--muted); margin-bottom: .6rem; }
.card { width: clamp(120px, 20vw, 190px); border-radius: 12px; box-shadow: 0 16px 34px rgba(0,0,0,.5);
  animation: deal .55s cubic-bezier(.2,.9,.25,1.15) both; }
.slot.right .card { animation-delay: .12s; }
@keyframes deal {
  0% { transform: translateY(-60px) rotateY(90deg) scale(.9); opacity: 0; }
  100% { transform: none; opacity: 1; }
}
.card.win { box-shadow: 0 0 0 3px var(--gold), 0 0 38px rgba(255,214,102,.65), 0 16px 34px rgba(0,0,0,.5);
  animation: deal .55s cubic-bezier(.2,.9,.25,1.15) both, glow 1.8s ease-in-out .7s infinite alternate; }
.card.lose { filter: saturate(.55) brightness(.78); transform: scale(.95); }
@keyframes glow { to { box-shadow: 0 0 0 3px var(--gold), 0 0 60px rgba(255,214,102,.9), 0 16px 34px rgba(0,0,0,.5); } }
.vs { width: 76px; height: 76px; border-radius: 50%; display: grid; place-items: center; margin: 0 auto;
  font-family: 'Cinzel', serif; font-weight: 800; font-size: 1.3rem; color: #2b1d02;
  background: radial-gradient(circle at 35% 30%, #fbe7a6, #d9a22c 70%); border: 3px solid #f7dc8f;
  box-shadow: 0 8px 22px rgba(0,0,0,.45); }
.vs.war { background: radial-gradient(circle at 35% 30%, #ff9a9a, #b3182f 70%); color: #fff; border-color: #ffb3b3;
  animation: shake .5s ease .2s; }
@keyframes shake { 25% { transform: rotate(-10deg) scale(1.1); } 75% { transform: rotate(10deg) scale(1.1); } }

.banner { margin: 1.3rem auto 0; text-align: center; font-weight: 600; font-size: 1.05rem;
  padding: .7rem 1.2rem; border-radius: 999px; width: fit-content; max-width: 100%;
  animation: rise .45s ease .35s both; }
.banner.you { background: rgba(227,184,74,.16); color: #ffe39a; border: 1px solid rgba(227,184,74,.55); }
.banner.cpu { background: rgba(239,111,127,.14); color: #ffc2ca; border: 1px solid rgba(239,111,127,.5); }
.banner.idle { background: rgba(0,0,0,.25); color: var(--muted); border: 1px solid rgba(255,255,255,.12); }
@keyframes rise { from { opacity: 0; transform: translateY(8px); } }

/* War zone */
.warzone { margin-top: 1.4rem; padding-top: 1.1rem; border-top: 1px dashed rgba(239,111,127,.45); }
.warzone .title { text-align: center; font-family: 'Cinzel', serif; font-weight: 800; letter-spacing: .3em;
  color: #ff8d9b; font-size: 1.1rem; margin-bottom: .8rem; }
.warrow { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: .6rem; margin-bottom: .8rem; }
.spread { display: flex; justify-content: center; align-items: center; }
.spread img { width: clamp(46px, 7vw, 72px); border-radius: 5px; margin-left: -26px; box-shadow: 0 6px 14px rgba(0,0,0,.45); }
.spread img:first-child { margin-left: 0; }
.spread img.reveal { width: clamp(64px, 10vw, 100px); margin-left: 8px; animation: deal .5s ease both; }
.spread .none { color: var(--muted); font-size: .8rem; letter-spacing: .08em; padding: 0 12px; }
.spread.cpu img { margin-left: 0; margin-right: -26px; }
.spread.cpu img:last-child { margin-right: 0; }
.spread.cpu img.reveal { margin-right: 8px; }
.spread img.win { box-shadow: 0 0 0 3px var(--gold), 0 0 30px rgba(255,214,102,.8); }
.warrow .n { font-size: .7rem; letter-spacing: .2em; color: var(--muted); text-transform: uppercase; }

/* Game over */
.finale { margin-top: 1.2rem; text-align: center; padding: 1.6rem 1rem; border-radius: 22px;
  border: 1px solid var(--gold-soft); background: linear-gradient(180deg, rgba(227,184,74,.16), rgba(0,0,0,.25));
  animation: rise .6s ease both; }
.finale h2 { font-family: 'Cinzel', serif; color: var(--gold); letter-spacing: .12em; margin: 0 0 .3rem; font-size: 2rem; }
.finale p { color: var(--cream); margin: 0; }

/* Log */
.log { display: flex; flex-direction: column; gap: .45rem; }
.logrow { display: grid; grid-template-columns: 70px 1fr auto; align-items: center; gap: .8rem;
  background: rgba(0,0,0,.22); border: 1px solid rgba(255,255,255,.06); border-radius: 12px; padding: .45rem .8rem; }
.logrow .rn { font-family: 'Cinzel', serif; color: var(--muted); font-size: .85rem; }
.logrow .pair { display: flex; align-items: center; gap: .5rem; }
.logrow .pair img { width: 38px; border-radius: 3px; box-shadow: 0 2px 5px rgba(0,0,0,.4); }
.logrow .pair span { color: var(--muted); font-size: .75rem; }
.pill { font-size: .75rem; font-weight: 600; padding: .2rem .65rem; border-radius: 99px; white-space: nowrap; }
.pill.you { background: rgba(227,184,74,.2); color: #ffe39a; }
.pill.cpu { background: rgba(239,111,127,.18); color: #ffc2ca; }
.pill.war { background: #b3182f; color: #fff; margin-left: .3rem; }

/* Stat tiles */
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .7rem; }
.tile { background: rgba(0,0,0,.22); border: 1px solid rgba(255,255,255,.07); border-radius: 14px; padding: .8rem 1rem; }
.tile .k { font-size: .7rem; letter-spacing: .18em; text-transform: uppercase; color: var(--muted); }
.tile .v { font-size: 1.6rem; font-weight: 700; color: var(--cream); margin-top: .15rem; }

[data-testid="stTabs"] button p { font-family: 'Cinzel', serif; letter-spacing: .08em; }

@media (max-width: 640px) {
  .scoreboard { grid-template-columns: 1fr 1fr; }
  .center-info { grid-column: 1 / -1; order: -1; }
  .stack { display: none; }
  .seat .count { font-size: 1.6rem; }
  .vs { width: 54px; height: 54px; font-size: 1rem; }
  .table { padding: 1.2rem .5rem; }
  .warrow { gap: .2rem; }
  .spread img { width: 30px; margin-left: -22px; }
  .spread.cpu img { margin-right: -22px; }
  .spread img.reveal { width: 52px; margin-left: 4px; }
  .spread.cpu img.reveal { margin-right: 4px; }
  .warrow .n { font-size: .6rem; letter-spacing: .1em; }
  .logrow { grid-template-columns: 44px 1fr auto; }
}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)


# ----------------------------------------------------------------- state ---
if "game" not in st.session_state:
    st.session_state.game = None
if "record" not in st.session_state:
    st.session_state.record = {"wins": 0, "losses": 0, "ties": 0}
if "back" not in st.session_state:
    st.session_state.back = "Crimson"
if "settings" not in st.session_state:
    st.session_state.settings = {"name": "Player", "rounds": 100}


# --------------------------------------------------------------- helpers ---
def card_img(card, css_class: str = "card", extra: str = "") -> str:
    return (
        f'<img class="{css_class} {extra}" src="{card_image(*card)}" '
        f'alt="{card_name(card)}" title="{card_name(card)}">'
    )


def back_img(css_class: str = "card", extra: str = "") -> str:
    return f'<img class="{css_class} {extra}" src="{card_back(st.session_state.back)}" alt="Face-down card">'


def pile_html(count: int) -> str:
    if count == 0:
        return '<div class="stack"><div class="empty"></div></div>'
    layers = min(1 + count // 5, 7)
    back = card_back(st.session_state.back)
    imgs = "".join(
        f'<img src="{back}" style="left:{i * 0.6}px; top:{-i * 1.8 + 12}px" alt="">' for i in range(layers)
    )
    return f'<div class="stack">{imgs}</div>'


def start_game(name: str, rounds: int) -> None:
    st.session_state.settings = {"name": name, "rounds": rounds}
    st.session_state.game = new_game(name, rounds)


def record_result(game: dict) -> None:
    """Add a finished game to the match record exactly once."""
    if game["status"] == "playing" or game.get("recorded"):
        return
    game["recorded"] = True
    if game["winner"] == game["player_name"]:
        st.session_state.record["wins"] += 1
        game["celebrate"] = True
    elif game["winner"] == "Computer":
        st.session_state.record["losses"] += 1
    else:
        st.session_state.record["ties"] += 1


def advance(game: dict, rounds: int | None) -> None:
    played = 0
    while game["status"] == "playing" and (rounds is None or played < rounds):
        play_round(game)
        played += 1
    record_result(game)


# --------------------------------------------------------------- sidebar ---
with st.sidebar:
    st.markdown('<p class="brand brand-sm">WAR ROYALE</p>', unsafe_allow_html=True)
    st.write("")
    rec = st.session_state.record
    st.markdown('<div class="eyebrow">Match record</div>', unsafe_allow_html=True)
    w, l, t = st.columns(3)
    w.metric("Wins", rec["wins"])
    l.metric("Losses", rec["losses"])
    t.metric("Ties", rec["ties"])

    if st.session_state.game is not None:
        st.selectbox(
            "Card back",
            list(CARD_BACKS),
            index=list(CARD_BACKS).index(st.session_state.back),
            key="back_sidebar",
            on_change=lambda: st.session_state.update(back=st.session_state.back_sidebar),
        )
        if st.button("New game", width="stretch"):
            st.session_state.game = None
            st.rerun()

    with st.expander("How to play"):
        st.write(
            "Each player starts with 26 cards. Every round both players flip "
            "their top card, and the higher rank takes both. Aces are high.\n\n"
            "**Tie? It's War.** Each player lays up to three cards face down, then "
            "flips one more. The higher card takes the whole pot. Wars can chain.\n\n"
            "The game ends when someone runs out of cards, or when the round "
            "limit is reached (most cards wins)."
        )


# ----------------------------------------------------------- landing page ---
game = st.session_state.game

if game is None:
    fan_cards = [(14, "Spades"), (13, "Hearts"), (12, "Clubs"), (11, "Diamonds"), (14, "Hearts")]
    angles = [-28, -14, 0, 14, 28]
    fan = "".join(
        f'<img src="{card_image(*c)}" style="transform: rotate({a}deg); animation-delay:{i * 0.08}s" alt="">'
        for i, (c, a) in enumerate(zip(fan_cards, angles))
    )
    st.html(
        f'<div class="hero"><div class="eyebrow">The classic card duel</div>'
        f'<h1 class="brand">WAR ROYALE</h1>'
        f'<div class="fan">{fan}</div>'
        f'<p class="tag">Flip, battle and conquer. The higher card takes the pot, and ties '
        f'spark an all-out war. Win all 52 cards to claim the crown.</p></div>'
    )

    _, middle, _ = st.columns([1, 1.4, 1])
    with middle:
        with st.form("setup", border=True):
            name = st.text_input("Your name", value=st.session_state.settings["name"], max_chars=20)
            rounds = st.select_slider(
                "Round limit", options=ROUND_CHOICES, value=st.session_state.settings["rounds"]
            )
            back = st.selectbox(
                "Card back", list(CARD_BACKS), index=list(CARD_BACKS).index(st.session_state.back)
            )
            deal = st.form_submit_button("Shuffle & Deal", type="primary", width="stretch")
        if deal:
            st.session_state.back = back
            start_game(name, int(rounds))
            st.rerun()
    st.stop()


# -------------------------------------------------------------- game page ---
player = game["player_name"]
p_count = len(game["player_deck"])
c_count = len(game["computer_deck"])
total = max(p_count + c_count, 1)
displayed_round = game["rounds"] + (game["status"] == "playing")
last = game["last_round"]

record_result(game)
if game.get("celebrate"):
    st.balloons()
    game["celebrate"] = False

st.html(
    f'<div class="scoreboard">'
    f'<div class="seat">{pile_html(p_count)}<div><div class="who">{player}</div>'
    f'<div class="count">{p_count}</div><div class="sub">CARDS</div></div></div>'
    f'<div class="center-info"><div class="eyebrow">Round</div>'
    f'<div class="round">{min(displayed_round, game["round_limit"])} / {game["round_limit"]}</div>'
    f'<div class="share"><div class="p" style="width:{p_count / total * 100:.1f}%"></div>'
    f'<div class="c" style="width:{c_count / total * 100:.1f}%"></div></div>'
    f'<div class="sub" style="margin-top:.45rem;color:var(--muted);font-size:.75rem">'
    f'⚔️ {game["wars"]} war{"s" if game["wars"] != 1 else ""} fought</div></div>'
    f'<div class="seat right">{pile_html(c_count)}<div><div class="who">Computer</div>'
    f'<div class="count">{c_count}</div><div class="sub">CARDS</div></div></div>'
    f'</div>'
)

# Battle table.
if last is None:
    duel = (
        f'<div class="duel"><div class="slot"><div class="label">{player}</div>{back_img()}</div>'
        f'<div class="vs">VS</div>'
        f'<div class="slot right"><div class="label">Computer</div>{back_img()}</div></div>'
        f'<div class="banner idle">Your deck is shuffled. Flip your first card!</div>'
    )
else:
    you_won = last["winner"] == player
    cpu_won = last["winner"] == "Computer"
    p_cls = "win" if you_won and not last["war_count"] else ("lose" if cpu_won and not last["war_count"] else "")
    c_cls = "win" if cpu_won and not last["war_count"] else ("lose" if you_won and not last["war_count"] else "")
    is_war = bool(last["war_count"])
    duel = (
        f'<div class="duel"><div class="slot"><div class="label">{player}</div>'
        f'{card_img(last["player_opening"], extra=p_cls)}</div>'
        f'<div class="vs {"war" if is_war else ""}">{"WAR" if is_war else "VS"}</div>'
        f'<div class="slot right"><div class="label">Computer</div>'
        f'{card_img(last["computer_opening"], extra=c_cls)}</div></div>'
    )

    if is_war:
        rows = []
        for i, ((pw, cw), (p_down, c_down)) in enumerate(
            zip(last["war_cards"], last["war_facedown"]), start=1
        ):
            final = i == len(last["war_cards"])
            out = '<span class="none">Out of cards</span>'
            p_rev = card_img(pw, "reveal", "win" if final and you_won else "") if pw else out
            c_rev = card_img(cw, "reveal", "win" if final and cpu_won else "") if cw else out
            rows.append(
                f'<div class="warrow"><div class="spread">{back_img("", "") * p_down}{p_rev}</div>'
                f'<div class="n">War {i}</div>'
                f'<div class="spread cpu">{c_rev}{back_img("", "") * c_down}</div></div>'
            )
        title = "WAR!" if last["war_count"] == 1 else f"{'DOUBLE' if last['war_count'] == 2 else 'MEGA'} WAR!"
        duel += f'<div class="warzone"><div class="title">⚔️ {title} ⚔️</div>{"".join(rows)}</div>'

    if last["winner"] == "Draw":
        duel += '<div class="banner idle">Both players ran dry mid-war. It\'s a draw!</div>'
    elif you_won:
        duel += f'<div class="banner you">🏆 You take the pot: +{last["cards_awarded"]} cards</div>'
    else:
        duel += f'<div class="banner cpu">The computer takes the pot: {last["cards_awarded"]} cards</div>'

# Alternate the wrapper tag each round so the browser re-creates the cards
# and replays the deal animation.
tag = "section" if game["rounds"] % 2 else "div"
st.html(f'<{tag} class="table">{duel}</{tag}>')

st.write("")

# Controls / finale.
if game["status"] == "playing":
    a, b, c = st.columns([2, 1, 1])
    if a.button("Flip cards", type="primary", width="stretch", icon=":material/style:"):
        advance(game, 1)
        st.rerun()
    if b.button("Play 10", width="stretch", icon=":material/fast_forward:"):
        advance(game, 10)
        st.rerun()
    if c.button("Skip to end", width="stretch", icon=":material/skip_next:"):
        advance(game, None)
        st.rerun()
else:
    if game["winner"] == player:
        head, msg = "VICTORY", f"{player} wins with {p_count} of {total} cards in {game['rounds']} rounds."
    elif game["winner"] == "Computer":
        head, msg = "DEFEAT", f"The computer wins with {c_count} of {total} cards in {game['rounds']} rounds."
    else:
        head, msg = "STALEMATE", f"Dead even after {game['rounds']} rounds."
    reason = "Round limit reached." if game["status"] == "limit" else "A deck ran out."
    st.html(f'<div class="finale"><h2>{head}</h2><p>{msg}</p><p class="eyebrow" style="margin-top:.5rem">{reason}</p></div>')
    st.write("")
    _, mid, _ = st.columns([1, 1, 1])
    if mid.button("Play again", type="primary", width="stretch", icon=":material/replay:"):
        start_game(st.session_state.settings["name"], st.session_state.settings["rounds"])
        st.rerun()

# Insights.
history = game["history"]
if history:
    st.write("")
    momentum, log, stats = st.tabs(["Momentum", "Round log", "Stats"])

    with momentum:
        you_label = player if player != "Computer" else f"{player} (you)"
        st.line_chart(
            {
                "Round": list(range(0, len(history) + 1)),
                you_label: [26] + [h["player_count"] for h in history],
                "Computer": [26] + [h["computer_count"] for h in history],
            },
            x="Round",
            y=[you_label, "Computer"],
            color=["#e3b84a", "#ef6f7f"],
            height=280,
        )

    with log:
        recent = history[-12:]
        first = len(history) - len(recent) + 1
        rows = []
        for offset, item in reversed(list(enumerate(recent))):
            won = item["winner"] == player
            pill = (
                f'<span class="pill {"you" if won else "cpu"}">'
                f'{"You" if won else item["winner"]} +{item["cards_awarded"]}</span>'
            )
            if item["war_count"]:
                pill += f'<span class="pill war">WAR ×{item["war_count"]}</span>'
            rows.append(
                f'<div class="logrow"><div class="rn">R{first + offset}</div>'
                f'<div class="pair">{card_img(item["player_opening"], "")}<span>vs</span>'
                f'{card_img(item["computer_opening"], "")}</div><div>{pill}</div></div>'
            )
        st.html(f'<div class="log">{"".join(rows)}</div>')

    with stats:
        won_rounds = sum(h["winner"] == player for h in history)
        biggest = max(h["cards_awarded"] for h in history)
        streak = best = 0
        for h in history:
            streak = streak + 1 if h["winner"] == player else 0
            best = max(best, streak)
        peak = max(h["player_count"] for h in history)
        tiles = [
            ("Rounds won", f"{won_rounds}/{len(history)}"),
            ("Win rate", f"{won_rounds / len(history):.0%}"),
            ("Best streak", best),
            ("Biggest pot", biggest),
            ("Peak pile", peak),
            ("Wars", game["wars"]),
        ]
        st.html(
            '<div class="tiles">'
            + "".join(f'<div class="tile"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in tiles)
            + "</div>"
        )
