import itertools
import random

from collections import defaultdict

welcome_message = """Hi Players
Welcome to “The Game of Dice"
============================
++ Rules of the Game

- The order in which the users roll the dice is decided randomly at the start of the game.

- If a player rolls the value "6" then they immediately get another chance to roll again and move
ahead in the game.

- If a player rolls the value "1" two consecutive times then they are forced to skip their next turn
as a penalty.
============================
"""

dice_choices = list(range(1, 7))

player_roll_history = defaultdict(lambda: [])


def get_int_input(message):
    """
        Function to get whole number as input
    :param message:
    :return:
    """
    number = input(message)
    if number.isnumeric():
        return int(number)
    else:
        print('Please provide a whole number input.')
        return get_int_input(message)


def get_roll_input(player_name):
    """
        Function to get chr 'r' as input
    :param player_name:
    :return:
    """
    inp = input(player_name + " its your turn (press ‘r’ to roll the dice): ")

    if inp.lower() == 'r':
        return True
    else:
        return get_roll_input(player_name)


def pre_roll_rules(player_name):
    """
        Function to apply all the post roll rule
    :param player_name:
    :return:
    """
    consecutive_ones_rule = True
    if len(player_roll_history[player_name]) >= 2 and player_roll_history[player_name][-2:] == [1, 1]:
        print(f"{player_name} chance will be skipped as he got two consecutive 1's")
        consecutive_ones_rule = False
    return consecutive_ones_rule


def post_roll_rules(player_name, rolled_number, threshold_points, curr_point):
    """
        Function to apply all the post roll rule
    :param player_name:
    :param rolled_number:
    :return:
    """
    extra_points = 0
    if rolled_number == 6:
        print(f'{player_name} gets another chance as he rolled a 6!!!')
        extra_points += roll_dice(player_name, threshold_points, curr_point+rolled_number)
    return extra_points


def roll_dice(player_name, threshold_points, curr_point):
    """
        Function to return a random rolled value with all the rules of the game applied
    :param player_name:
    :return:
    """
    if pre_roll_rules(player_name):
        choice = random.choice(dice_choices)  # Having pure randomness in computer system is not possible
        print(f'{player_name} rolled a {str(choice)}')
        if (curr_point + choice) < threshold_points:
            choice += post_roll_rules(player_name, choice, threshold_points, curr_point)
        return choice
    else:
        return 0


def print_ranks(points_map, ranking_map):
    for player, points in points_map.items():
        print(f"{player} scored {points} points and got a rank of {ranking_map[player]}")


def game():
    """
        The Core function where everything starts and comes to an end.
    :return:
    """
    print(welcome_message)
    num_of_players = get_int_input("Please input the number of players: ")
    threshold_points = get_int_input("Please input the threshold points: ")

    # create players
    players_list = [f"Player {player_num}" for player_num in list(range(1, num_of_players+1))]
    random.shuffle(players_list)  # Having pure randomness in computer system is not possible

    print("Starting the Game...")

    points_map = {player: 0 for player in players_list}
    ranking_map = defaultdict(lambda: "Did not finish!")
    current_rank = 0

    try:
        for player in itertools.cycle(players_list):
            if player not in ranking_map:
                get_roll_input(player)
                points_map[player] += roll_dice(player, threshold_points, points_map[player])
                if points_map[player] >= threshold_points:
                    # the player finished
                    current_rank += 1
                    ranking_map[player] = current_rank
                    print(f"Congrats! {player} you have finished with rank {current_rank}!")

                if current_rank >= num_of_players-1:
                    break
    finally:
        print('Game Finished!! Below is the ranking table')
        print_ranks(points_map, ranking_map)


if __name__ == '__main__':
    game()
