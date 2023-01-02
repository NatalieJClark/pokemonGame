import random
import requests
import csv
import os


# Function to generate random Pokémon
def random_pokemon():
    # Generate a random number between 1 and 151 to use as the Pokémon ID number
    pokemon_id = random.randint(1, 151)
    # Use the Pokémon API to get a Pokémon based on its ID number
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    response = requests.get(url)
    pokemon = response.json()
    # Create dictionary of Pokémon data
    return{
        'Name': pokemon['name'].capitalize(),
        'Id': pokemon['id'],
        'Height': pokemon['height'],
        'Weight': pokemon['weight'],
        'Moves': len(pokemon['moves']),
    }


# Function to play the game
def game():
    # Use global statement to give score variables scope throughout the program
    global player_score, opponent_score
    # Print round number
    print(f'\nROUND {turn + 1}:')
    # Generate 3 random Pokémon for the player to choose from, and print them
    pokemon1 = random_pokemon()
    pokemon2 = random_pokemon()
    pokemon3 = random_pokemon()
    print(f'Your Pokemon options are:\n'
          f'1. {pokemon1["Name"]}\n'
          f'2. {pokemon2["Name"]}\n'
          f'3. {pokemon3["Name"]}\n')

    # Create pokemon_choice variable
    pokemon_choice = {}
    # Use try and except, in a while loop, to detect when the user enters incorrect data
    # Continue loop when user input is incorrect, and break out of loop when user input is correct
    while True:
        try:
            pokemon_choice = int(input('Which Pokémon would you like to use? (1/2/3): '))
        except ValueError:
            print("\nSorry, I didn't understand that.  Please enter a digit.")
            continue
        if pokemon_choice != 1 and pokemon_choice != 2 and pokemon_choice != 3:
            print('\nYou must enter a valid pokemon option, to play!')
            continue
        else:
            break

    # Create player_pokemon variable
    player_pokemon = {}
    # Assign user pokemon_choice to player_pokemon
    if pokemon_choice == 1:
        player_pokemon = pokemon1
    elif pokemon_choice == 2:
        player_pokemon = pokemon2
    elif pokemon_choice == 3:
        player_pokemon = pokemon3

    # Display stats of the user's chosen Pokémon
    print(f'\nOk, your Pokémon is {player_pokemon["Name"]}:\n'
          f' Id = {player_pokemon["Id"]}\n'
          f' Weight = {player_pokemon["Weight"]}kg\n'
          f' Height = {player_pokemon["Height"]}cm\n'
          f' No. of moves = {player_pokemon["Moves"]}')

    # If even numbered round, the opponent chooses a random stat
    if ((turn + 1) % 2) == 0:
        random_num = random.randint(0, 3)
        if random_num == 0:
            stat_choice = 'Id'
        elif random_num == 1:
            stat_choice = 'Weight'
        elif random_num == 2:
            stat_choice = 'Height'
        else:
            stat_choice = 'Moves'

        print(f'\nThis time your opponent chooses the stat!  They choose: {stat_choice}')

    # If odd numbered round, the user is asked to choose the stat
    else:
        # Ask the user which stat they want to use
        stat_choice = input('\nHighest stat wins!  Which stat would you like to play? '
                            '(Id/Height/Weight/Moves): ').strip().capitalize()

        # If statement to deal with user input error
        if stat_choice != 'Id' and stat_choice != 'Height' and stat_choice != 'Weight' and stat_choice != 'Moves':
            print('\nYou must enter a valid stat, to play!')
            stat_choice = input('\nWhich stat would you like to play? '
                                '(Id/Height/Weight/Moves): ').strip().capitalize()

    # Get a random Pokémon for their opponent and print its stat
    opponent_pokemon = random_pokemon()

    if stat_choice == 'Height':
        print(f'Your opponent\'s Pokémon is {opponent_pokemon["Name"]}\n'
              f' {stat_choice} = {opponent_pokemon[stat_choice]}cm')
    elif stat_choice == 'Weight':
        print(f'Your opponent\'s Pokémon is {opponent_pokemon["Name"]}\n'
              f' {stat_choice} = {opponent_pokemon[stat_choice]}kg')
    else:
        print(f'Your opponent\'s Pokémon is {opponent_pokemon["Name"]}\n'
              f' {stat_choice} = {opponent_pokemon[stat_choice]}')

    # Assign player and opponent stat, and compare to decide who wins
    player_stat = player_pokemon[stat_choice]
    opponent_stat = opponent_pokemon[stat_choice]

    if player_stat > opponent_stat:
        print(f'\nYou win!'),
        player_score += 1
    elif player_stat == opponent_stat:
        print('\nIt\'s a draw!'),
    else:
        print('\nSorry, you lose.  Better luck next time!'),
        opponent_score += 1

    print(f'{username} {player_score} : Opponent {opponent_score}')


# Function to update scoreboard file and print from it
def scoreboard():
    # Assign header and column variables for csv
    field_names = ['username', 'match results', 'round results']
    data = [
        {'username': username, 'match results': match_results, 'round results': round_results},
    ]

    # Open CSV file and append user scores
    with open('scoreboard.csv', 'a', newline='') as csv_file:
        spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
        file_path = 'scoreboard.csv'
        # only write headers if file is empty
        if os.stat(file_path).st_size == 0:
            spreadsheet.writeheader()
        spreadsheet.writerows(data)

    # Open csv file and read users player stats
    with open('scoreboard.csv', 'r') as csv_file:
        spreadsheet = csv.DictReader(csv_file)
        match_scores = []
        round_scores = []
        for row in spreadsheet:
            # If statement, to target rows in the csv that have user's username as the 'username' value
            # then append the match results from these rows, as integers, to the match_scores list
            # and append the round results from these rows, as integers, to the round_scores list
            if username == row['username']:
                match = row['match results']
                match_scores.append(int(match))
                score = row['round results']
                round_scores.append(int(score))

    # Print player stats
    total_matches = len(match_scores)
    matches_won = sum(match_scores)
    win_rate = round(matches_won/total_matches*100)
    highest_score = max(round_scores)
    print(f'Thanks for playing, {username}!  Here are your player stats:\n'
          f' Total matches played = {total_matches}\n'
          f' Total matches won = {matches_won}\n'
          f' Match win rate = {win_rate}%\n'
          f' Highest score = {highest_score}')

# Assign variables for starting scores
player_score = 0
opponent_score = 0
match_results = 0
round_results = 0

# Find out user's username
username = input(f'What is your username? ')
if username == '':
    username = input(f'Please enter your username to play: ')

# Find out if user wants to play the game, and if they do, how many rounds they want
play_choice = input(f'Hi {username}, welcome to Pokémon Top Trumps!  Would you like to play? (y/n): ').strip().lower()
if play_choice == 'y' or play_choice == 'yes':
    num_rounds = {}
    # Use try and except, in a while loop, to detect when the user enters incorrect data
    # Continue loop when user input is incorrect, and break out of loop when user input is correct
    while True:
        try:
            num_rounds = int(input('How many rounds would you like to play? (1/3/5): '))
        except ValueError:
            print("\nSorry, I didn't understand that.")
            continue
        if num_rounds != 1 and num_rounds != 3 and num_rounds != 5:
            print('\nYou must enter a valid number of rounds, to play!')
            continue
        else:
            break

    print(f'\nOk let\'s play!  Best of {num_rounds} rounds, wins ...')

    # Loop through game() function for chosen number of rounds
    for turn in range(num_rounds):
        game()

    # Print final match score
    print(f'\nFINAL SCORE = {username} {player_score} : Opponent {opponent_score}')

    # Add final player_score to round_results variable
    round_results += player_score

    # Compare final scores to decide champion, print result, and adjust match_results variable
    if player_score > opponent_score:
        print(f'{username} is the champion!\n')
        match_results += 1
    elif player_score < opponent_score:
        print(f'Opponent is the champion, better luck next time!\n')
        match_results += 0
    else:
        print(f'It\'s a draw!\n')
        match_results += 0

    scoreboard()


# If user doesn't want to play, print message
elif play_choice == 'n' or play_choice == 'no':
    print('Ok, maybe next time!')

else:
    print('I wasn\'t expecting that answer!')
