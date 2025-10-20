from boat_case import BoatCase
class Boat:
    def __init__(self, name : str):
        self.cases = []
        self.name = name


    def add_case(self, case : BoatCase):
        self.cases.append(case)