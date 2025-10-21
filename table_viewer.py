import string
class TableViewer:
    def __init__(self):
        # {'letter':'','','',...} 10 spaces that are equivalent to the
        self.data = {c: [''] * 10 for c in string.ascii_uppercase[:10]}
        self.game_message = ''

    def update_table(self, failed_shots, boat_shots, sunken_boats):
        # add the failed shots to it
        for fs in failed_shots:
            self.data[fs.nb[0].upper()][int(fs.nb[1:]) - 1] = "x"

        # add the boat shots to it
        for bs in boat_shots:
            self.data[bs.nb[0].upper()][int(bs.nb[1:]) - 1] = "#"

        # add the sunk boat to it
        for sb in sunken_boats:
            self.data[sb.nb[0].upper()][int(sb.nb[1:]) - 1] = "O"


    def render(self):
        table_boat = ""

        # generate table dynamically
        # each line of it
        for i in range(10 + 1):
            # first line
            table_boat += "+---" * 11 + "+\n"

            # part 1 generate the indexes
            # add the first number
            # add empty space for the first line
            if i == 0:
                table_boat += "|   |"
            # special to print 10 without extra space
            elif i == 10:
                table_boat += "| " + str(i) + "|"
            # add the number for the line
            else:
                table_boat += "| " + str(i) + " |"

            # part 2 generate the caracters line only for first line
            # all the nexts lines
            if i == 0:
                # create a list from A to J and then go throught all letters
                for c in string.ascii_uppercase[:10]:
                    table_boat += " " + c + " |"
                table_boat += "\n"
            # part 3 generate the playable/played cases
            # for all others line exept line 0/first line
            if i > 0:
                # create a list from A to J and then go throught all letters
                for c in string.ascii_uppercase[:10]:
                    # get the cases for the letter
                    case = self.data[c]

                    # if the case empty add empty space
                    if case[i - 1] == "":
                        table_boat += "   |"
                    # not empty : add the character to game
                    else:
                        table_boat += " " + case[i - 1] + " |"
                        # line break
                table_boat += "\n"
        # last line
        table_boat += "+---" * 11 + "+\nJeu: " + self.game_message
        #clear game_message
        self.game_message = ""
        return table_boat