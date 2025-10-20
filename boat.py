from boat_case import BoatCase
class Boat:
    def __init__(self, name : str):
        self.cases = []
        self.name = name


    #add
    def add_case(self, case : BoatCase):
        self.cases.append(case)


    def add_multiple_cases(self, cases_list : list):
        self.cases += cases_list


    #creator
    def create_multiple_cases(self, *cases):
        for case_str in cases:
            self.cases.append(BoatCase(case_str))


    #setter
    def set_case(self, cases_list : list):
        self.cases = cases_list