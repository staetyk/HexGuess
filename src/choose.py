import random


class Color():
    def __init__(self, _hex: str):
        self.hex = int(_hex, 16)
        self.name = "#" + _hex.lstrip("0x").upper().zfill(6)
        self.rgb = [int(_hex[2:4],16), int(_hex[4:6],16), int(_hex[6:],16)]

def randcolor():
    return Color("0x" + hex(random.randrange(0, 0x1000000)).lstrip("0x").zfill(6))

def create(hard: bool = False):
    correct = randcolor()
    answers = [(correct, True)]

    while len(answers) < 4:
        new = randcolor()
        for x in answers:
            dif = lambda a,b : abs(a-b)
            Z = iter(x[0].rgb)
            for y in new.rgb:
                z = next(Z)
                if dif(y,z) < (8 if hard else 16):
                    break
            else:
                continue
            break
        else:
            answers.append((new, False))

    answers = dict(answers)
    options = {}
    keys = list(set(answers.keys()))
    for x in keys:
        options.update({x.name : answers[x]})

    return tuple((options, correct.hex))