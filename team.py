from __future__ import annotations
from data_structures.referential_array import ArrayR
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats, Constants
from player import Player
from typing import Collection, Union, TypeVar
from data_structures.hash_table import *
from data_structures.array_sorted_list import *
from data_structures.linked_list import *

T = TypeVar("T")

class Team:
    counter = 1
    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity:   O(player + statistic*(comp + _linear_probe)) where player is the number of players in the 
                                    players attribute, statistic is the team statistics to add to the hash table
            Worst Case Complexity:  O(player + statistic*(comp + _linear_probe)) where player is the number of players in the 
                                    players attribute, statistic is the team statistics to add to the hash table
        """
        self.number = Team.counter
        self.name = team_name
        self.statistics = LinearProbeTable[TeamStats,int]()
        self.players = ArraySortedList(Constants.TEAM_MAX_PLAYERS)

        for player in players:
            self.add_player(player)

        for statistic in TeamStats:
            if statistic == TeamStats.LAST_FIVE_RESULTS:
                self.statistics[statistic.value] = LinkedList()
            else:
                self.statistics[statistic.value] = 0

        Team.counter += 1

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity:   O(statistic*(comp + _linear_probe)) where statistic is the team statistics to reset in the 
                                    hash table
            Worst Case Complexity:  O(statistic*(comp + _linear_probe)) where statistic is the team statistics to reset in the 
                                    hash table
        """
        for statistic in TeamStats:
            if statistic == TeamStats.LAST_FIVE_RESULTS:
                self.statistics[statistic.value].clear()
            else:
                self.statistics[statistic.value] = 0

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity:   O(comp) when player added is the middle element
            Worst Case Complexity:  O(log(n) * comp) when all elements in the list are checked, n is the length 
                                    of the list
        """
        player.set_add_order(len(self))
        self.players.add(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(n) when the player removed is at the start of the list, where n is all of 
                                    the elements in the list to shuffle to the left
        """
        self.players.remove(player)

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.number
    
    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(n*comp + m) 
                                    where n is the players in the team, m is the players matching the given position
        """
        if self.players.is_empty():
            return None
        
        # return all players if position is none
        if position is None:
            ret = ArrayR(self.players.length)
            i = 0
            for player in self.players:
                ret[i] = player
                i += 1
            return ret

        found_players = [player for player in self.players if player.position == position]
    
        # return none if position given can't be found
        if len(found_players) == 0:
            return None
        
        # return players with given position
        ret = ArrayR(len(found_players))

        i = 0
        for player in found_players:
            ret[i] = player
            i += 1

        return ret
    
    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(1)
        """
        return self.statistics
    
    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity:   O(hash(key) + N*comp) where key is the length of the key to be hashed, N is the 
                                    table size
            Worst Case Complexity:  O(hash(key) + N*comp) where key is the length of the key to be hashed, N is the 
                                    table size
        """
        if self.statistics[TeamStats.GAMES_PLAYED.value] == 0:
            return None
        return self.statistics[TeamStats.LAST_FIVE_RESULTS.value]

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        #fit 2085 student
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity:   O(hash(key) + (N*comp)) where key is the length of the key to be hashed, N is the 
                                    table size
            Worst Case Complexity:  O(hash(key) + (hash(key) + N*comp) + (N*comp)) where key is the length of the key to be hashed, N is the 
                                    table size
        """
        if statistic == TeamStats.WINS:
            self.statistics[TeamStats.POINTS.value] += 3
            self.add_last_five_results(GameResult.WIN)
        elif statistic == TeamStats.LOSSES:
            self.statistics[TeamStats.POINTS.value] = value
            self.add_last_five_results(GameResult.LOSS)
        elif statistic == TeamStats.GOALS_FOR:
            self.statistics[TeamStats.POINTS.value] += value
        elif statistic == TeamStats.GOALS_AGAINST:
            self.statistics[TeamStats.POINTS.value] -= value
        elif statistic == TeamStats.DRAWS:
            self.statistics[TeamStats.POINTS.value] += value
            self.add_last_five_results(GameResult.DRAW)
        self.statistics[statistic.value] = value
        self.statistics[TeamStats.GAMES_PLAYED.value] += 1
        self.statistics[TeamStats.GOALS_DIFFERENCE.value] = self.statistics[TeamStats.GOALS_FOR.value] - self.statistics[TeamStats.GOALS_AGAINST.value]

    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity:   O(hash(key) + N*comp) where key is the length of the key to be hashed, N is the 
                                    table size
            Worst Case Complexity:  O(hash(key) + N*comp) where key is the length of the key to be hashed, N is the 
                                    table size
        """
        return self.statistics[statistic.value]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(1)
        """
        return self.players.length

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        ret = "Name:",self.get_name()
        ret += " | Points:",self.statistics[TeamStats.POINTS.value]
        ret += " | Wins:",self.statistics[TeamStats.WINS.value]
        ret += " | Goals for:",self.statistics[TeamStats.GOALS_FOR.value]
        ret += " | Goals difference:",self.statistics[TeamStats.GOALS_DIFFERENCE.value]
        return ret

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)

    def add_last_five_results(self, game_result: GameResult) -> None:
        """
        Complexity:
            Best Case Complexity:   O(hash(key) + N*comp) where key is the length of the key to be hashed, N is the 
                                    table size
            Worst Case Complexity:  O(hash(key) + N*comp) where key is the length of the key to be hashed, N is the 
                                    table size
        """
        results = self.statistics[TeamStats.LAST_FIVE_RESULTS.value]
        results.append(game_result)
        if len(results) > 5:
            results.delete_at_index(0)

    def __gt__(self,other) -> bool:
        if self.statistics[TeamStats.POINTS.value] > other.statistics[TeamStats.POINTS.value]:
            return False
        elif self.statistics[TeamStats.POINTS.value] == other.statistics[TeamStats.POINTS.value]:
            if self.statistics[TeamStats.GOALS_DIFFERENCE.value] > other.statistics[TeamStats.GOALS_DIFFERENCE.value]:
                return False
            elif self.statistics[TeamStats.GOALS_DIFFERENCE.value] > other.statistics[TeamStats.GOALS_DIFFERENCE.value]:
                if self.statistics[TeamStats.GOALS_FOR.value] > other.statistics[TeamStats.GOALS_FOR.value]:
                    return False
                elif self.statistics[TeamStats.GOALS_FOR.value] == other.statistics[TeamStats.GOALS_FOR.value]:
                    if ord(self.name[0]) > ord(other.name[0]):
                        return False
        return True
        
    def __lt__(self, other) -> bool:
        if self.statistics[TeamStats.POINTS.value] < other.statistics[TeamStats.POINTS.value]:
            return False
        elif self.statistics[TeamStats.POINTS.value] == other.statistics[TeamStats.POINTS.value]:
            if self.statistics[TeamStats.GOALS_DIFFERENCE.value] > other.statistics[TeamStats.GOALS_DIFFERENCE.value]:
                return False
            elif self.statistics[TeamStats.GOALS_DIFFERENCE.value] > other.statistics[TeamStats.GOALS_DIFFERENCE.value]:
                if self.statistics[TeamStats.GOALS_FOR.value] < other.statistics[TeamStats.GOALS_FOR.value]:
                    return False
                elif self.statistics[TeamStats.GOALS_FOR.value] == other.statistics[TeamStats.GOALS_FOR.value]:
                    if ord(self.name[0]) < ord(other.name[0]):
                        return False
        return True
        
    def __ge__(self, other) -> bool:
        return self > other or self == other
    
    def __le__(self,other) -> bool:
        return self < other or self == other
    
    def __eq__(self,other) -> bool:
        if not isinstance(other, Team):
            return False
        
        return (self.name == other.name and self.players == other.players and self.statistics == other.statistics 
                and self.get_number() == other.get_number())