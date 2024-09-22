from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from dataclasses import dataclass
from team import Team
from typing import Generator, Union

from constants import Constants, TeamStats, PlayerStats
from data_structures.array_sorted_list import *
from data_structures.linked_list import *
from game_simulator import *

@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        self.count = 0
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity:   O(1)
        Worst Case Complexity:  O(1)
        """
        return self

    def __next__(self):
        """
        Complexity:
        Best Case Complexity:   O(1)
        Worst Case Complexity:  O(1)
        """
        if self.count is not None:
            if self.count <= 0:
                raise StopIteration
        
        ret = self.games[self.count]
        self.count -= 1
        return ret
        


class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity:   O(team + i) where team is the teams in the leaderboard, i is the amount of possible 
                                    games between the teams
            Worst Case Complexity:  O(team + i) where team is the teams in the leaderboard, i is the amount of possible 
                                    games between the teams
        """
        self.current_week = 0
        self.teams = teams
        self.teams_length = len(teams)
        self.leaderboard = ArraySortedList(Constants.MAX_NUM_TEAMS)
        for team in self.teams:
            self.leaderboard.add(team)
        self.schedule = LinkedList()
        generated_schedule = self._generate_schedule()
        for i in range(len(generated_schedule)):
            self.schedule.append(generated_schedule[i])

    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:`
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity:   O(n + games*(home*_linear_probe + away*_linear_probe + result_stats*(comp + _linear_probe))) 
                                    when there are no results at the end of the game, where n is the weeks of games, 
                                    games is the number of games in the week, home is the players in the home team, 
                                    away is the players in the away team, result_stats is the statistics in the ResultStats 
                                    enum
            Worst Case Complexity:  O(n + games*(home*_linear_probe + away*_linear_probe + 
                                    result_stats*(comp + _linear_probe + players*(away*comp + comp + _linear_probe)))) 
                                    when player is found in away team and their stats need to be changed,
                                    where n is the weeks of games, games is the number of games in the week, home is the 
                                    players in the home team, away is the players in the away team,
                                    result_stats is the statistics in the ResultStats enum, players is the players that appear
                                    in the ResultStat key's value
        """
        for n in range(len(self.schedule)):
            current_game = self.get_next_game()
            for game in current_game:
                home_team = game.home_team
                away_team = game.away_team

                # increment games played for teams & players involved
                home_team.statistics[TeamStats.GAMES_PLAYED.value] += 1
                away_team.statistics[TeamStats.GAMES_PLAYED.value] += 1
                for player in home_team.get_players():
                    player.statistics[PlayerStats.GAMES_PLAYED.value] += 1
                for player in away_team.get_players():
                    player.statistics[PlayerStats.GAMES_PLAYED.value] += 1

                result = GameSimulator.simulate(home_team,away_team)
                
                for statistic in ResultStats:
                    # add goals for to home team & against for away team
                    if statistic == ResultStats.HOME_GOALS:
                        home_team.statistics[TeamStats.GOALS_FOR.value] += result[statistic.value]
                        away_team.statistics[TeamStats.GOALS_AGAINST.value] += result[statistic.value]

                    # add goals for away team & against for home team
                    elif statistic == ResultStats.AWAY_GOALS:
                        away_team.statistics[TeamStats.GOALS_FOR.value] += result[statistic.value]
                        home_team.statistics[TeamStats.GOALS_AGAINST.value] += result[statistic.value]

                    elif result[statistic.value]:
                        for player_name in result[statistic.value]:
                            continue_searching = True

                            #find player in home team or away team
                            for player in home_team.players:
                                if player.get_name() == player_name:
                                    player_object = player
                                    continue_searching = False

                            if continue_searching:
                                for player in away_team.players:
                                    if player.get_name() == player_name:
                                        player_object = player

                            # increment player goals
                            if statistic == ResultStats.GOAL_SCORERS:
                                player_object.statistics[PlayerStats.GOALS.value] += 1
                            # increment player assists
                            elif statistic == ResultStats.GOAL_ASSISTS:
                                player_object.statistics[PlayerStats.ASSISTS.value] += 1
                            # increment player tackles
                            elif statistic == ResultStats.TACKLES:
                                player_object.statistics[PlayerStats.TACKLES.value] += 1
                            #increment player interception
                            elif statistic == ResultStats.INTERCEPTIONS:
                                player_object.statistics[PlayerStats.INTERCEPTIONS.value] += 1
            self.current_week += 1

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(n + insert) where n is the amount of elements to be shuffled to the left in the list
                                    
        """
        orig_week_index = orig_week - 1
        games_to_move = self.schedule[orig_week_index]
        self.schedule.delete_at_index(orig_week_index)

        if new_week == None:
            # delay game to end of season
            self.schedule.append(games_to_move)
        else:
            # move delayed game to given week
            self.schedule.insert(new_week - 1, games_to_move)

    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity:   O(n + comp) where n is the weeks between first week and the requested week of games
            Worst Case Complexity:  O(n + comp) where n is the weeks between first week and the requested week of games
        """
        current_week_game = self.schedule[self.current_week]
        
        if current_week_game is None or len(current_week_game) == 0:
            return None
        
        return current_week_game

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity:   O(teams + _linear_probe)
                                    where teams is the teams in the leaderboard, stats is the 
                                    team statistics to get the value from
            Worst Case Complexity:  O(teams + _linear_probe)
                                    where teams is the teams in the leaderboard, stats is the 
                                    team statistics to get the value from
        """
        teams_data = []

        for team in self.leaderboard: 
            statistics = team.get_statistics()
            print(team.__str__())
            teams_data.append([
                team.get_name(),
                statistics[TeamStats.GAMES_PLAYED.value],
                statistics[TeamStats.POINTS.value],
                statistics[TeamStats.WINS.value],
                statistics[TeamStats.DRAWS.value],
                statistics[TeamStats.LOSSES.value],
                statistics[TeamStats.GOALS_FOR.value],
                statistics[TeamStats.GOALS_AGAINST.value],
                statistics[TeamStats.GOALS_DIFFERENCE.value],
                team.get_last_five_results()
            ])

        return teams_data

    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity:O(1)
        """
        return self.teams

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(1)
        """
        return self.teams_length

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
