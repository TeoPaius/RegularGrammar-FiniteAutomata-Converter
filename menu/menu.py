class Menu:
    def __init__(self, grammar, automata):
        self.grammar = grammar
        self.automata = automata
        self.commands = {0: ("Grammar N", grammar.getN_str),
                         1: ("Grammar E", grammar.getE_str),
                         2: ("Grammar P", grammar.getP_str),
                         3: ("Grammar S", grammar.getS_str),
                         4: ("Grammar is Regular", grammar.isRegular),
                         5: ("Grammar to Automata", grammar.toAutomata_str),
                         6: ("Automata Q", automata.getQ_str),
                         7: ("Automata E", automata.getE_str),
                         8: ("Automata q0", automata.getQ0_str),
                         9: ("Automata R", automata.getR_str),
                         10: ("Automata F", automata.getF_str),
                         11: ("Automata to Grammar", automata.toRegGrammar_str)}

    def __str__(self):
        ret = ""
        for (key, value) in self.commands.items():
            ret += str(key) + ". " + value[0] + '\n'
        return ret

    def execute(self, command):
        if command not in self.commands.keys():
            print("Invalid command")
        else:
            return self.commands[command][1]()