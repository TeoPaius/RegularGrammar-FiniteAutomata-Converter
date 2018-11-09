from menu.menu import Menu
from model.finiteAuto import FiniteAuto
from model.regGramar import RegGrammar

if __name__ == '__main__':
    r = RegGrammar()
    a = FiniteAuto()
    r.readFromFile("inputs/grammar.txt")
    a.readFromFile("inputs/automata.txt")
    # r.readFromKeyboard()
    print(r)
    print(r.isRegular())
    print(a)

    menu = Menu(r, a)
    while True:
        print(str(menu))
        cmd = input("Insert command: ")
        print(menu.execute(int(cmd)))
        print('')


