import sys




class Production:
    def __init__(self, right=None, left=None):
        if left is None:
            self.left = []
        if right is None:
            self.right = []
        self.left = right
        self.right = left

    def __str__(self):
        return str(self.left) + " -> " + str(self.right) + '\n'


class RegGrammar:

    def __init__(self):
        self.N = []
        self.E = []
        self.P = []
        self.S = None
        self.epsRule = False

    def readFromFile(self, fileName):
        try:
            with open(fileName) as file:
                line = file.readline()
                self.N = [i.strip('\n') for i in line.split(',')]
                line = file.readline()
                self.E = [i.strip('\n') for i in line.split(',')]
                self.S = self.N[0]

                for line in file:
                    left = [i.strip('\n') for i in line.split('-')[0].split(' ') if i != '']
                    for i in left:
                        if i not in self.N and i not in self.E:
                            raise Exception("INVALID INPUT LEFT")
                    right = [i.strip('\n') for i in line.split('-')[1].split(' ') if i != '']
                    for i in right:
                        if i not in self.N and i not in self.E and i != "eps":
                            raise Exception("INVALID INPUT RIGHT")
                    self.P.append(Production(left, right))
        except Exception as e:
            print("GRAMMAR EXCEPTION")
            print(str(e))
            sys.exit(-1)

    def getN_str(self):
        return str(self.N)

    def getE_str(self):
        return str(self.E)

    def getP_str(self):
        return str("".join([str(i) for i in self.P]))

    def getS_str(self):
        return str(self.S)

    def __str__(self):
        return "N: " + str(self.N) + "\nE: " + str(self.E) + "\nP: " + str(
            "".join([str(i) for i in self.P])) + "\nS: " + str(self.S) + '\n'

    def readFromKeyboard(self):
        try:
            self.N = [i.strip('\n') for i in input("N (S first): ").split(',')]
            self.E = [i.strip('\n') for i in input("E: ").split(',')]
            self.S = self.N[0]
            nr = int(input("Nr of productions: "))
            print("Enter productions of form: \"left - right\"")
            for i in range(0, nr):
                line = input()
                left = [i.strip('\n') for i in line.split('-')[0].split(' ') if i != '']
                for i in left:
                    if i not in self.N and i not in self.E:
                        raise Exception("INVALID INPUT")
                right = [i.strip('\n') for i in line.split('-')[1].split(' ') if i != '']
                for i in right:
                    if i not in self.N and i not in self.E:
                        raise Exception("INVALID INPUT")
                self.P.append(Production(left, right))
        except Exception as e:
            print(str(e))
            sys.exit(-1)

    def isRegular(self):
        self.epsRule = False
        for i in self.P:
            if len(i.left) != 1:
                return False
            if len(i.right) > 2 or len(i.right) == 0:
                return False
            if len(i.right) == 1:
                if i.right[0] == "eps":
                    if i.left[0] == self.S:
                        self.epsRule = True
                    else:
                        return False
                    continue
                if i.right[0] not in self.E:
                    return False
            if len(i.right) == 2:
                if i.right[0] not in self.E or i.right[1] not in self.N:
                    return False
        if self.epsRule:
            for i in self.P:
                if self.S in i.right:
                    return False

        return True

    def toAutomata(self):
        from model.finiteAuto import FiniteAuto, Transition

        if not self.isRegular():
            return "NOT REGULAR"

        automata = FiniteAuto()
        automata.E = self.E
        automata.q0 = self.S
        automata.Q.extend(self.N)

        if self.epsRule:
            automata.F.append(self.S)

        hasK = False
        for i in self.P:
            t = Transition()
            t.left = i.left[0]
            if len(i.right) == 1:
                t.right = 'K'
                t.symbol = i.right[0]
                if not hasK:
                    automata.F.append('K')
                    automata.Q.append('K')
                    hasK = True
                if i.right == "eps":
                    automata.F.append(self.S)
            if len(i.right) == 2:
                t.right = i.right[1]
                t.symbol = i.right[0]
            if t.left == self.S and t.right == 'K' and t.symbol == "eps":
                continue
            automata.R.append(t)
        return automata

    def toAutomata_str(self):
        return str(self.toAutomata())
