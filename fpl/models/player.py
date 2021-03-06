import requests

from ..constants import API_URLS
from ..utils import team_converter, position_converter


def get_additional(player_id):
    """Returns additional information about the player with the given
    player ID.

    :param int player_id: A player's ID
    """
    players = requests.get(API_URLS["players"]).json()
    for player in players:
        if player["id"] == player_id:
            return player
    return []


class Player():
    """A class representing a player in the Fantasy Premier League."""
    def __init__(self, player_id, additional=None):
        self.player_id = player_id
        self._specific = self._get_specific()
        self._additional = additional or get_additional(player_id)

        #: The amount of goals assisted by the player.
        self.assists = self._additional["assists"]
        #: The amount of bonus points the player has scored.
        self.bps = self._additional["bps"]
        #: The amount of clean sheets the player has had.
        self.clean_sheets = self._additional["clean_sheets"]
        #: Information about the player's upcoming fixture.
        self.explain = self._specific["explain"]
        #: The player's first name.
        self.first_name = self._additional["first_name"]
        #: List of the player's upcoming fixtures.
        self.fixtures = self._specific["fixtures"]
        #: List of the player's closest three upcoming fixtures.
        self.fixtures_summary = self._specific["fixtures_summary"]
        #: The player's form.
        self.form = self._additional["form"]
        #: The player's points in the current gameweek.
        self.gameweek_points = self._additional["event_points"]
        #: The player's price change in the current gameweek.
        self.gameweek_price_change = self._additional["cost_change_event"]
        #: The player's transfers in in the current gameweek.
        self.gameweek_transfers_in = self._additional["transfers_in_event"]
        #: The player's transfers out in the current gameweek.
        self.gameweek_transfers_out = self._additional["transfers_out_event"]
        #: The amount of goals scored by the player.
        self.goals = self._additional["goals_scored"]
        #: List of the player's performance in fixtures of the current season.
        self.history = self._specific["history"]
        #: List of a summary of the player's performance in previous seasons.
        self.history_past = self._specific["history_past"]
        #: List of the player's performance in his three most recent games.
        self.history_summary = self._specific["history_summary"]
        #: The amount of minutes the player has played.
        self.minutes = self._additional["minutes"]
        #: The player's web name.
        self.name = self._additional["web_name"]
        #: News about the player.
        self.news = self._additional["news"]
        #: The amount of penalties the player has missed.
        self.penalties_missed = self._additional["penalties_missed"]
        #: The type of player the player is (1, 2, 3 or 4).
        self.player_type = self._additional["element_type"]
        #: The amount of points a player has scored this season.
        self.points = self._additional["total_points"]
        #: The position that the player plays in.
        self.position = position_converter(self.player_type)
        #: The amount of points the player scores per game on average.
        self.ppg = self._additional["points_per_game"]
        #: The player's current price.
        self.price = self._additional["now_cost"] / 10.0
        #: The amount of red cards the player has received.
        self.red_cards = self._additional["red_cards"]
        #: The amount of saves the player has made.
        self.saves = self._additional["saves"]
        #: The player's second name.
        self.second_name = self._additional["second_name"]
        #: The percentage of users the player is selected by.
        self.selected_by = float(self._additional["selected_by_percent"])
        #: The status of the player, which can be available, injured or ...
        self.status = self._additional["status"]
        #: The player's squad number.
        self.squad_number = self._additional["squad_number"]
        #: The ID of the team the player plays for.
        self.team_id = self._additional["team"]
        #: The team the player currently plays for.
        self.team = team_converter(self.team_id)
        #: The player's transfers in in the current season.
        self.transfers_in = self._additional["transfers_in"]
        #: The player's transfers out in the current season.
        self.transfers_out = self._additional["transfers_out"]
        #: The amount of yellow cards the player has received.
        self.yellow_cards = self._additional["yellow_cards"]

    def _get_specific(self):
        """Returns the player with the specific player_id."""
        return requests.get(API_URLS["player"].format(self.player_id)).json()

    @property
    def games_played(self):
        """Returns the amount of games a player has played in."""
        return sum([1 for fixture in self.fixtures if fixture["minutes"] > 0])

    @property
    def pp90(self):
        """Returns the amount of points a player scores per 90 minutes played.
        """
        if self.minutes == 0:
            return 0
        return self.points / float(self.minutes)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.position, self.team)
