from copy import deepcopy
import string
from boat import Boat
from boat_case import BoatCase
from typing import List
#"lf" means local to function #TODO REMOVE IT


def are_all_boat_sunk(boat_list_lf):
    """
    Function to detect if all the boats are sunk and the game should finish
    :param boat_list_lf: the list of boats in game
    :return: boolean to check if the game should finish
    """
    #for each boat
    for boat_lf in boat_list_lf:
        #for each case
        for boat_case in boat_lf.cases:
            #if the case is not hit (basically is false)
            if not boat_case.hit:
                return False
    #if all the cases are hit (are true, return true)
    return True


def check_and_hit_boat_position(boat_list_lf, shot_case, boat_shots, sunken_boats, failed_shots):
    """
    ths function will handle the hit to the boat
    :param boat_list_lf:  list of boats
    :param shot_case: the case attacked by the player
    :param boat_shots: list of all shot that landed on a boat
    :param sunken_boats: list of all sunken boats
    :param failed_shots: list of objects of failed shots that landed on the sea
    :return: n/a
    """
    #get global var
    global var_msg

    player_shot_try = BoatCase(shot_case)
    #foreach boat
    for boat_lf in boat_list_lf:
        #foreach case
        for boat_case in boat_lf.cases:
            #if the shot case is the same as the boat case
            if boat_case.case_nb == player_shot_try.case_nb:
                #if the case got already hit
                if boat_case.hit:
                    var_msg = 'Cette case à dejà été bombardée'
                    #get out of the function
                    return
                #if not hit, hit it
                else:
                    #form the message
                    var_msg = "Le "+boat_lf.name+" à été bombardé!"
                    #hit it
                    boat_case.hit = True

                    #add the shot to the list of shooted boats if not present
                    boat_shots.append(player_shot_try) if not player_shot_try.in_list(boat_shots) else None

                    #if the boat got all the case hit
                    if all(bcs.hit for bcs in boat_lf.cases):
                        #message
                        var_msg += '\n Le '+boat_lf.name+' vient de tomber'

                        #remove the cases from the shot list and add to the sunk list
                        for case_lf in boat_lf.cases:
                            #remove from the shot boats (add back to list each boatcase if the boatcase name from boat_shots  is not the same as case name given by user)
                            boat_shots = [bc for bc in boat_shots if bc.case_nb != case_lf.case_nb]
                            #insert into sunken boats
                            sunken_boats.append(case_lf)
                    #exit the program
                    return
    failed_shots.append(player_shot_try) if not player_shot_try.in_list(failed_shots) else None

    var_msg = 'Le tir est tompé dans l\'ocean'



def render_table(failed_shots_lf, boat_shots_lf, sunken_boats):


    data = {c: [''] * 10 for c in string.ascii_uppercase[:10]}



    #add the failed shots to it
    for fs in failed_shots_lf:
        data[fs.case_nb[0].upper()][int(fs.case_nb[1:])-1] = "x"

    #add the boat shots to it
    for bs in boat_shots_lf:
        data[bs.case_nb[0].upper()][int(bs.case_nb[1:])-1] = "#"

    #add the sunk boat to it
    for sb in sunken_boats:
        data[sb.case_nb[0].upper()][int(sb.case_nb[1:])-1] = "O"

    table_boat = ""


    #generate table dynamically
    #each line of it
    for i in range(10+1):
        #first line
        table_boat += "+---"*11+"+\n"

        #part 1 generate the indexes
        #add the first number
        # add empty space for the first line
        if i==0:
            table_boat += "|   |"
        # special to print 10 without extra space
        elif i==10:
            table_boat += "| " + str(i) + "|"
        #add the number for the line
        else:
            table_boat += "| " + str(i) + " |"

        #part 2 generate the caracters line only for first line
        #all the nexts lines
        if i==0:
            #create a list from A to J and then go throught all letters
            for c in string.ascii_uppercase[:10]:
                table_boat += " "+c+" |"
            table_boat += "\n"
        #part 3 generate the playable/played cases
        #for all others line exept line 0/first line
        if i>0:
            #create a list from A to J and then go throught all letters
            for c in string.ascii_uppercase[:10]:
                #get the cases for the letter
                case = data[c]

                #if the case empty add empty space
                if case[i-1] == "":
                    table_boat += "   |"
                #not empty : add the character to game
                else:
                    table_boat += " "+case[i-1]+" |"
                    #line break
            table_boat += "\n"
    #last line
    table_boat += "+---" * 11 + "+"

    #print with pandas
    print(table_boat)


def main():
    # declare a global var to the message to the user and set initial text
    global var_msg
    #var_msg = 'Bienvenue au jeu de bataille navale !'

    # define the list for the shots
    failed_shots : List[BoatCase] = []
    sunken_boats : List[BoatCase] = []
    boat_shots : List[BoatCase] = []

    # define the boats
    #POO
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
        # render the table with all shots
        render_table(failed_shots, boat_shots, sunken_boats)
        # game message
        print('JEU : ' + var_msg)
        var_msg = 'n/a'
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
            boatlist = [aircraft_carrier, cruiser, destroyer, submarine, torpedo_boat]

            # check a boat at this case and if present hit it
            check_and_hit_boat_position(boatlist, case, boat_shots, sunken_boats, failed_shots)

            # check if all boats are sunk
            if are_all_boat_sunk(boatlist):
                print('Bravo! vous avez detruit tous les bateaux')
                break
        # given any irregular case
        else:
            var_msg = 'case incorrecte'


if __name__ == '__main__':
    var_msg = 'Bienvenue au jeu de bataille navale !'
    main()