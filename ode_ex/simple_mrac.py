from typing import Callable


class SimpleMARC:
    def __init__(self, order_, input_gain_) -> None:
        self.order = order_
        self.h = input_gain_

        self.model_fnc = {}
        self.ref_param = {}
        self.est_param = {}

    def AddModelDynamics(self, name: str, 
                        model_fnc: Callable[[float, float], float]):
        self.model_fnc[name] = model_fnc

    def SetRefParams(self, name: str, param: float):
        self.ref_param[name] = param

if __name__=="__main__":
    pass
