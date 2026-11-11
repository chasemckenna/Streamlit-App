import streamlit as st

from war_game import card_name, new_game, play_round


st.set_page_config(page_title="War Card Game", page_icon="🂠", layout="wide")
st.title("War: The Card Game")
st.write(
	"Play the classic head-to-head card game. Draw one card each round; the "
	"higher rank wins both cards. Ties trigger a War automatically."
)

if "game" not in st.session_state:
	st.session_state.game = None

with st.sidebar:
	st.header("Game setup")
	with st.form("game_setup"):
		player_name = st.text_input("Your name", value="Player", max_chars=24)
		round_limit = st.number_input(
			"Round limit", min_value=1, max_value=1000, value=100, step=25
		)
		start_game = st.form_submit_button("Start or restart game", type="primary")

	if start_game:
		st.session_state.game = new_game(player_name, int(round_limit))

	with st.expander("How to play"):
		st.write(
			"Each player starts with 26 cards. Play a round to reveal the top "
			"card from each pile. The higher rank collects both cards. If the "
			"ranks tie, each player puts up to three cards face down and then "
			"reveals another card. The game ends when a player runs out of "
			"cards or reaches the round limit."
		)

game = st.session_state.game
if game is None:
	st.info("Set your name and round limit, then start a game.")
else:
	player_count = len(game["player_deck"])
	computer_count = len(game["computer_deck"])
	displayed_round = game["rounds"] + (game["status"] == "playing")
	st.subheader(f"Round {displayed_round} of {game['round_limit']}")

	player_metric, computer_metric, war_metric = st.columns(3)
	player_metric.metric(f"{game['player_name']} cards", player_count)
	computer_metric.metric("Computer cards", computer_count)
	war_metric.metric("Wars so far", game["wars"])

	if game["last_round"] is not None:
		last_round = game["last_round"]
		player_column, computer_column = st.columns(2)
		with player_column:
			with st.container(border=True):
				st.caption(game["player_name"])
				st.markdown(f"### {card_name(last_round['player_opening'])}")
		with computer_column:
			with st.container(border=True):
				st.caption("Computer")
				st.markdown(f"### {card_name(last_round['computer_opening'])}")

		if last_round["war_count"]:
			st.warning(
				f"War! The tie was resolved after {last_round['war_count']} "
				"war round(s)."
			)
			for war_index, (player_war_card, computer_war_card) in enumerate(
				last_round["war_cards"], start=1
			):
				player_reveal = (
					card_name(player_war_card) if player_war_card else "No card"
				)
				computer_reveal = (
					card_name(computer_war_card) if computer_war_card else "No card"
				)
				st.write(
					f"War reveal {war_index}: {player_reveal} vs. {computer_reveal}"
				)

		if last_round["winner"] == "Draw":
			st.info("Neither player could reveal another card, so the round is a draw.")
		else:
			st.success(
				f"{last_round['winner']} won the round and collected "
				f"{last_round['cards_awarded']} cards."
			)

	if game["status"] == "playing":
		if st.button("Play round", type="primary", width="stretch"):
			play_round(game)
			st.rerun()
	elif game["status"] == "finished":
		if game["winner"] == "Tie":
			st.info("The game ended in a tie because both players ran out of cards.")
		else:
			st.success(f"Game over. {game['winner']} collected all the cards!")
	elif game["status"] == "limit":
		if game["winner"] == "Tie":
			st.info("Round limit reached with an equal number of cards.")
		else:
			st.info(
				f"Round limit reached. {game['winner']} leads with "
				f"{max(player_count, computer_count)} cards."
			)

	if game["history"]:
		st.subheader("Recent rounds")
		recent_rounds = game["history"][-10:]
		first_round_number = game["rounds"] - len(recent_rounds) + 1
		st.dataframe(
			[
				{
					"Round": first_round_number + index,
					game["player_name"]: card_name(item["player_opening"]),
					"Computer": card_name(item["computer_opening"]),
					"Winner": item["winner"],
					"Cards collected": item["cards_awarded"],
				}
				for index, item in enumerate(recent_rounds)
			],
			hide_index=True,
			width="stretch",
		)
