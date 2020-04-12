import itertools
import random
from yattag import Doc


class ExercisesGenerator:

    # notes - how many notes should be produced per measure
    def __init__(self, notes):
        # right, left
        self._hands = 'RL'
        # bass, ton, slap, none
        self._hits = 'BTSN'
        self._notes = notes
        self._combinations = []
        self._exercises_count = 0

    def generate_combinations(self, shuffle=False):
        hands_combinations = [''.join(item) for item in itertools.product(self._hands, repeat=self._notes)]
        hits_combinations = [''.join(item) for item in itertools.product(self._hits, repeat=self._notes)]

        if len(self._combinations) > 0:
            self._combinations = []
        for hit in hits_combinations:
            for hand in hands_combinations:
                self._combinations.append((hit, hand))

        if shuffle:
            random.shuffle(self._combinations)

    def generateHTML(self, output_file):
        if len(self._combinations) == 0:
            self.generate_combinations(True)
        doc, tag, text = Doc().tagtext()

        styles_content = '.pattern{display:block}.measure{display:inline-block;border-right:5px solid #000;height:50px;width:216px}.measure-first{border-left:5px solid #000}.note{border:5px solid #000;border-radius:50px;width:20px;height:20px;margin:0 10px;display:inline-block;font-size:17px;text-align:center}.bass{background-color:#000;color:#fff}.slap{background-color:red}.none{border:1px solid #000;color:#fff;margin:0 14px}'

        self._exercises_count = 0
        with tag('html'):
            with tag('head'):
                with tag('style'):
                    text(styles_content)
            with tag('body'):
                for pattern in self._combinations:
                    if pattern[0] == 'NNNN':
                        continue
                    with tag('div', ('class', 'pattern')):
                        self._exercises_count += 1
                        for i in range(4):
                            measure_class = 'measure'
                            if i == 0:
                                measure_class += ' measure-first'
                            with tag('div', ('class', measure_class)):
                                for note in range(self._notes):
                                    hit = pattern[0][note]
                                    hand = pattern[1][note]
                                    note_class = 'note'
                                    if hit == 'B':
                                        note_class += ' bass'
                                    elif hit == 'T':
                                        note_class += ' tone'
                                    elif hit == 'S':
                                        note_class += ' slap'
                                    elif hit == 'N':
                                        note_class += ' none'
                                    with tag('div', ('class', note_class)):
                                        text(hand)

        result = doc.getvalue()
        with open(output_file, 'w') as file:
            file.write(result)


if __name__ == '__main__':
    ExercisesGenerator(4).generateHTML('./djembe_drillz.html')
