import sys


class Transition:
    def __init__(self, left= None, right = None, symbol = None):
        self.left = left
        self.right = right
        self.symbol = symbol

    def __str__(self):
        return str(self.left) + " --" + str(self.symbol) + "-- " + str(self.right) + '\n'



class FiniteAuto:
    def __init__(self):
        self.Q = []
        self.E = []
        self.R = []
        self.q0 = None
        self.F = []

    def __str__(self):
        return "Q: " + str(self.Q) + "\nE: " + str(self.E) + "\nF: " + str(self.F) + "\nR: " + str(
            "".join([str(i) for i in self.R])) + "\nq0: " + str(self.q0) + '\n'

    def getQ_str(self):
        return str(self.Q)

    def getE_str(self):
        return str(self.E)

    def getR_str(self):
        return str("".join([str(i) for i in self.R]))

    def getQ0_str(self):
        return str(self.q0)

    def getF_str(self):
        return str(self.F)

    def readFromFile(self, fileName):
        try:
            with open(fileName) as file:
                line = file.readline()
                self.Q = [i.strip('\n') for i in line.split(',')]
                line = file.readline()
                self.E = [i.strip('\n') for i in line.split(',')]
                self.q0 = self.Q[0]
                line = file.readline()
                self.F = [i.strip('\n') for i in line.split(',')]

                for line in file:
                    tokens = [i.strip('\n') for i in line.split(' ')]
                    if len(tokens) != 3:
                        raise Exception("PARSING ERROR")
                    if tokens[0] not in self.Q or tokens[2] not in self.Q:
                        raise Exception("INVALID STATE")
                    if tokens[1] not in self.E:
                        raise Exception("INVALID SYMBOL")
                    transition = Transition(tokens[0], tokens[2], tokens[1])
                    self.R.append(transition)

        except Exception as e:
            print("AUTOMATON EXCEPTION")
            print(str(e))
            sys.exit(-1)

    def readFromKeyboard(self):
        try:
            line = input("States: ")
            self.Q = [i.strip('\n') for i in line.split(',')]
            line = input("Symbols: ")
            self.E = [i.strip('\n') for i in line.split(',')]
            self.q0 = self.Q[0]
            line = input("Final states: ")
            self.F = [i.strip('\n') for i in line.split(',')]

            nrTrans = int(input("Nr of transitions (X a Y): "))

            for i in range(0, nrTrans):
                line = input()
                tokens = [i.strip('\n') for i in line.split(' ')]
                if len(tokens) != 3:
                    raise Exception("PARSING ERROR")
                if tokens[0] not in self.Q or tokens[2] not in self.Q:
                    raise Exception("INVALID STATE")
                if tokens[1] not in self.E:
                    raise Exception("INVALID SYMBOL")
                transition = Transition(tokens[0], tokens[2], tokens[1])
                self.R.append(transition)

        except Exception as e:
            print("AUTOMATON EXCEPTION")
            print(str(e))
            sys.exit(-1)

    def toRegGrammar(self):
        from model.regGramar import RegGrammar, Production

        grammar = RegGrammar()

        grammar.S = self.q0
        grammar.N = self.Q
        grammar.E = self.E

        for i in self.R:
            prod = Production()
            prod.left = [i.left]
            prod.right = [i.symbol, i.right]
            grammar.P.append(prod)
            if i.right == 'K':
                prod2 = Production()
                prod2.left = [i.left]
                prod2.right = [i.symbol]
                grammar.P.append(prod2)

        if self.q0 in self.F:
            prod = Production()
            prod.left = self.q0
            prod.right = ["eps"]

        return grammar

    def toRegGrammar_str(self):
        return str(self.toRegGrammar())