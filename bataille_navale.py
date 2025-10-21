import time
from copy import deepcopy
import string
from boat import Boat
from boat_case import BoatCase
from typing import List
from table_viewer import TableViewer


def are_all_boat_sunk(boat_list):
    """
    Function to detect if all the boats are sunk and the game should finish
    :param boat_list: the list of boats in game
    :return: boolean to check if the game should finish
    """
    #for each boat
    for boat in boat_list:
        #for each case
        for boat_case in boat.cases:
            #if the case is not hit (basically is false)
            if not boat_case.hit:
                return False
    #if all the cases are hit (are true, return true)
    return True


def check_and_hit_boat_position(boat_list, shot_case, boat_shots, sunken_boats, failed_shots):
    """
    ths function will handle the hit to the boat
    :param boat_list:  list of boats
    :param shot_case: the case attacked by the player
    :param boat_shots: list of all shot that landed on a boat
    :param sunken_boats: list of all sunken boats
    :param failed_shots: list of objects of failed shots that landed on the sea
    :return: n/a
    """
    #get global var
    #global var_msg

    player_shot_try = BoatCase(shot_case)
    #foreach boat
    for boat in boat_list:
        #foreach case
        for boat_case in boat.cases:
            #if the shot case is the same as the boat case
            if boat_case.case_nb == player_shot_try.case_nb:
                #if the case got already hit
                if boat_case.hit:
                    game_table.game_message = 'Cette case à dejà été bombardée'
                    #get out of the function
                    return
                #if not hit, hit it
                else:
                    #form the message
                    game_table.game_message = "Le "+boat.name+" à été bombardé!"
                    #hit it
                    boat_case.hit = True

                    #add the shot to the list of shooted boats if not present
                    boat_shots.append(player_shot_try) if not player_shot_try.in_list(boat_shots) else None

                    #if the boat got all the case hit
                    if all(bcs.hit for bcs in boat.cases):
                        #message
                        game_table.game_message += '\n Le '+boat.name+' vient de tomber'

                        #remove the cases from the shot list and add to the sunk list
                        for case in boat.cases:
                            #remove from the shot boats (add back to list each boatcase if the boatcase name from boat_shots  is not the same as case name given by user)
                            boat_shots = [bc for bc in boat_shots if bc.case_nb != case.case_nb]
                            #insert into sunken boats
                            sunken_boats.append(case)
                    #exit the program
                    return
    failed_shots.append(player_shot_try) if not player_shot_try.in_list(failed_shots) else None

    game_table.game_message = 'Le tir est tompé dans l\'ocean'


def main():
    #set initial message
    game_table.game_message = 'Bienvenue au jeu de bataille navale !'

    # define the list for the shots
    failed_shots : List[BoatCase] = []
    sunken_boats : List[BoatCase] = []
    boat_shots : List[BoatCase] = []

    # define the boats
    #create the aircraft carrier
    aircraft_carrier = Boat('aircraft_carrier')
    # define and add cases
    aircraft_carrier.create_multiple_cases('B2','C2','D2','E2','F2')


    # cruiser
    cruiser = Boat('cruiser')
    # define and add cases
    cruiser.create_multiple_cases('A4','A5','A6','A7')

    # destroyer
    destroyer = Boat('destroyer')
    # define and add cases
    destroyer.create_multiple_cases('C5', 'C6', 'C7')

    # submarine
    submarine = Boat('submarine')
    # define and add cases
    submarine.create_multiple_cases('H5', 'I5', 'J5')

    # torpedo_boat
    torpedo_boat = Boat('torpedo_boat')
    # define and add cases
    torpedo_boat.create_multiple_cases ('E9', 'F9')

    # execute in loop the game
    while True:
        #update the table
        game_table.update_table(failed_shots, boat_shots, sunken_boats)
        #render the table
        print(game_table.render())


        # game message
        game_table.game_message = 'n/a'

        print('-' * 30)

        # input
        case = input('Inserer la case à ataquer : ').upper()

        # check if the input case has between 2 and 3 chars, the first char is between A and J, and the 2 and 3 are digits, and the digits are between 1 and 10
        if (
                len(case) in (2, 3)
                # and case[0].isalpha()
                and case[0] in "ABCDEFGHIJ"
                and case[1:].isdigit()
                and 1 <= int(case[1:]) <= 10
        ):

            # create boat list
            boat_list = [aircraft_carrier, cruiser, destroyer, submarine, torpedo_boat]

            # check a boat at this case and if present hit it
            check_and_hit_boat_position(boat_list, case, boat_shots, sunken_boats, failed_shots)

            # check if all boats are sunk
            if are_all_boat_sunk(boat_list):
                game_table.update_table(failed_shots, boat_shots, sunken_boats)
                game_table.game_message += 'Bravo! vous avez detruit tous les bateaux'
                print(game_table.render())
                break
        # given any irregular case
        else:
            game_table.game_message = 'case incorrecte'


if __name__ == '__main__':
    #create a table POO
    game_table = TableViewer()
    game_table.game_message = 'Bienvenue au jeu de bataille navale !'
    main()