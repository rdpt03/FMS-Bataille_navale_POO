from copy import deepcopy
import pandas
import string
#"lf" means local to function


#define what is a boat :
template_boat = {'name':'','cases':[]}
template_boat_case = {'case_nb':'', 'hit':False}



#function to add cases to boat
def add_cases_to_boat(boat_lf, cases):
    """
    Function to add cases to the boat
    :param boat_lf: the boat list
    :param cases: the cases to add
    """
    for case_to_add in cases:
        #copy the template boat case
        boat_case = deepcopy(template_boat_case)
        #add the case num to the case of the boar
        boat_case['case_nb'] = case_to_add
        #add the case of the boat to the boat case list
        boat_lf['cases'].append(boat_case)


def are_all_boat_sunk(boat_list_lf):
    """
    Function to detect if all the boats are sunk and the game should finish
    :param boat_list_lf: the list of boats in game
    :return: boolean to check if the game should finish
    """
    #for each boat
    for boat_lf in boat_list_lf:
        #for each case
        for boat_case in boat_lf['cases']:
            #if the case is not hit (basically is false)
            if not boat_case['hit']:
                return False
    #if all the cases are hit (are true, return true)
    return True


def check_and_hit_boat_position(boat_list_lf, shot_case):
    """
    ths function will handle the hit to the boat
    :param boat_list_lf:  list of boats
    :param shot_case: the case attacked by the player
    :return: n/a
    """
    #get global var
    global var_msg

    #foreach boat
    for boat_lf in boat_list_lf:
        #foreach case
        for boat_case in boat_lf['cases']:
            #if the shot case is the same as the boat case
            if boat_case['case_nb'] == shot_case:
                #if the case got already hit
                if boat_case['hit']:
                    var_msg = 'Cette case à dejà été bombardée'
                    #get out of the function
                    return
                #if not hit, hit it
                else:
                    #form the message
                    var_msg = "Le "+boat_lf["name"]+" à été bombardé!"
                    #hit it
                    boat_case['hit'] = True

                    #add the shot to the list of shooted boats if not present
                    boat_shots.append(shot_case) if shot_case not in boat_shots else None

                    #if the boat got all the case hit
                    if all(bcs['hit'] for bcs in boat_lf['cases']):
                        #message
                        var_msg += '\n Le '+boat_lf['name']+' vient de tomber'

                        #remove the cases from the shot list and add to the sunk list
                        for case_lf in boat_lf['cases']:
                            boat_shots.remove(case_lf['case_nb'])
                            sunk_boats.append(case_lf['case_nb'])
                    #exit the program
                    return
    #if the hit failed (basicaccly no return where executed) (todo : test without condition alwasy to false
    failed_shots.append(shot_case) if shot_case not in failed_shots else None
    var_msg = 'Le tir est tompé dans l\'ocean'



def render_table(failed_shots_lf, boat_shots_lf, sunk_boats_lf):
    #Create the table with panda
    #create the dictionary base

    #data = {
    #    chr(c).upper() : ['' for _ in range(10)] for c in range(ord('a'),ord('j')+1)
    #}

    data = {c: [''] * 10 for c in string.ascii_uppercase[:10]}



    #add the failed shots to it
    for fs in failed_shots_lf:
        data[fs[0].upper()][int(fs[1:])-1] = "x"

    #add the boat shots to it
    for bs in boat_shots_lf:
        data[bs[0].upper()][int(bs[1:])-1] = "#"

    #add the sunk boat to it
    for sb in sunk_boats_lf:
        data[sb[0].upper()][int(sb[1:])-1] = "O"

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

if __name__ == '__main__':
    #declare a global var to the message to the user and set initial text
    global var_msg
    var_msg = 'Bienvenue au jeu de bataille navale !'

    #define the list for the shots
    failed_shots = []
    sunk_boats = []
    boat_shots = []

    # define the boats
    # aircraft_carrier
    aircraft_carrier = deepcopy(template_boat)
    aircraft_carrier['name'] = 'aircraft_carrier'
    # define and add cases
    add_cases_to_boat(aircraft_carrier, ['B2', 'C2', 'D2', 'E2', 'F2'])

    #cruiser
    cruiser = deepcopy(template_boat)
    cruiser['name'] = 'cruiser'
    # define and add cases
    add_cases_to_boat(cruiser, ['A4', 'A5', 'A6', 'A7'])

    # destroyer
    destroyer = deepcopy(template_boat)
    destroyer['name'] = 'destroyer'
    # define and add cases
    add_cases_to_boat(destroyer, ['C5', 'C6', 'C7'])

    # submarine
    submarine = deepcopy(template_boat)
    submarine['name'] = 'submarine'
    # define and add cases
    add_cases_to_boat(submarine, ['H5', 'I5', 'J5'])

    # torpedo_boat
    torpedo_boat = deepcopy(template_boat)
    torpedo_boat['name'] = 'torpedo_boat'
    # define and add cases
    add_cases_to_boat(torpedo_boat, ['E9', 'F9'])


    #execute in loop the game
    while True:
        #render the table with all shots
        render_table(failed_shots, boat_shots, sunk_boats)
        #game message
        print('JEU : '+var_msg)
        var_msg = 'n/a'
        print('-' * 30)
        #input
        case = input('Inserer la case à ataquer : ').upper()

        #check if the input case has between 2 and 3 chars, the first char is between A and J, and the 2 and 3 are digits, and the digits are between 1 and 10
        if (
                len(case) in (2, 3)
                #and case[0].isalpha()
                and case[0] in "ABCDEFGHIJ"
                and case[1:].isdigit()
                and 1 <= int(case[1:]) <= 10
        ):

            #create boat list
            boatlist = [aircraft_carrier,cruiser, destroyer, submarine, torpedo_boat]

            #check a boat at this case and if present hit it
            check_and_hit_boat_position(boatlist,case)

            #check if all boats are sunk
            if are_all_boat_sunk(boatlist):
                print('Bravo! vous avez detruit tous les bateaux')
                break
        #given any irregular case
        else:
            var_msg = 'case incorrecte'