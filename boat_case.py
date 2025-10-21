class BoatCase:
    def __init__(self,case_nb : str):
        self.case_nb = case_nb
        self.hit = False

    def in_list(self, boat_case_list : list):
        for e in boat_case_list:
            if e.case_nb == self.case_nb:
                return True
        return False
