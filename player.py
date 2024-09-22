from __future__ import annotations
from constants import PlayerPosition, PlayerStats
from data_structures.hash_table import *
from enum import auto, IntEnum

class Player:
    position_value = {
        PlayerPosition.GOALKEEPER: 1,
        PlayerPosition.DEFENDER: 2,
        PlayerPosition.MIDFIELDER: 3,
        PlayerPosition.STRIKER: 4
    }

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Returns:
            None

        Complexity:
            Best Case Complexity:  O(1)
            Worst Case Complexity: O(statistic) - where statistic is the PlayerStats enum values to 
                                    insert into the hash table

        """
        self.name = name
        self.position = position
        self.age = age
        self.statistics = LinearProbeTable[PlayerStats,int]()
        self.add_order = 0

        for statistic in PlayerStats:
            self.statistics[statistic.value] = 0

    def reset_stats(self) -> None:
        """`
        Reset the stats of the player

        Returns:
            None

        Complexity:
            Best Case Complexity:   O(statistic*_linear_probe) - where statistic is the player stats to reset
            Worst Case Complexity:  O(statistic*_linear_probe) - where statistic is the player stats to reset

        """
        for statistic in PlayerStats:
            self.statistics[statistic.value] = 0

    def get_name(self) -> str:
        """
        Get the name of the player

        Returns:
            str: The name of the player

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(1)
        """
        return self.name

    def get_position(self) -> PlayerPosition:
        """
        Get the position of the player

        Returns:
            PlayerPosition: The position of the player

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(1)
        """
        return self.position

    def get_statistics(self):
        """
        Get the statistics of the player

        Returns:
            statistics: The players' statistics

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(1)
        """
        return self.statistics

    def __setitem__(self, statistic: PlayerStats, value: int) -> None:
        """
        Set the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat
            value (int): The value of the stat

        Returns:
            None

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(_linear_probe)
        """
        self.statistics[statistic.value] = value

    def __getitem__(self, statistic: PlayerStats) -> int:
        """
        Get the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity:   O(1)
            Worst Case Complexity:  O(_linear_probe)
        """
        return self.statistics[statistic.value]

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity:
            Analysis not required.
        """
        ret = "Player name: " + self.name
        ret += " Player age: " + str(self.age)
        ret += " Player position: " + self.get_position().value
        ret += " Player statistics: "
        ret += self.get_statistics().__str__()
        return ret

    def __repr__(self) -> str:
        """Returns a string representation of the Player object.
        Useful for debugging or when the Player is held in another data structure."""
        return str(self)
    
    def set_add_order(self, add_order: int) -> None:
        """
            Best Case Complexity: O(1)
            Worst Case complexity O(1)
        """
        self.add_order = add_order
    
    def get_position_value(self) -> int:
        """
            Best Case Complexity: O(1)
            Worst Case complexity O(1)
        """
        return self.position_value[self.position]

    def __gt__(self,other) -> bool:
        if self.get_position_value() > other.get_position_value():
            return True
        elif self.get_position_value() == other.get_position_value():
            # return self.age > other.age
            return self.add_order > other.add_order
        return False
        
    def __lt__(self, other) -> bool:
        if self.get_position_value() < other.get_position_value():
            return True
        elif self.get_position_value() == other.get_position_value():
            # return self.age < other.age
            return self.add_order < other.add_order
        return False
        
    def __ge__(self, other) -> bool:
        return self > other or self == other
    
    def __le__(self,other) -> bool:
        return self < other or self == other
    
    def __eq__(self,other) -> bool:
        return self.position == other.position and self.age == other.age