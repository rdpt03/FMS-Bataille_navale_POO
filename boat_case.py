from typing import List

class BoatCase:
    def __init__(self,nb : str):
        self.nb = nb
        self.hit = False

    def in_list(self, boat_case_list : List["BoatCase"]):
        for e in boat_case_list:
            if e.nb == self.nb:
                return True
        return False
