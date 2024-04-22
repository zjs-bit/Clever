from Environment import *
from Player import *
from ActionSpace import * 

def main():

    e = GameEnvironment()
    p = Player(0,e,"Bill")
    a = ActionSpace()

    z = p.get_feasible_actions(a,e)

    print(z)

if __name__ == '__main__':
    main()