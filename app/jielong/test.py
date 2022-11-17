from pathlib import Path
idiom_path = str(Path(__file__).resolve().parent)+"\idiom.txt"

import random
jielong_EX=60
jielong_DEFAULT_DIFFICULTY="0"
def query_idiom(words):
    with open(idiom_path, 'r') as f:
        for i in set(f.readlines()):
            if words == i.strip():

                return True
    return False


def random_idiom():
    alpha_list = [chr(i) for i in range(65, 91)]
    temp_list = []
    with open(idiom_path, 'r') as f:
        for i in set(f.readlines()):
            if i.strip()[0] not in alpha_list:
                temp_list.append(i.strip())

    index = random.randint(0, len(temp_list) - 1)
    return temp_list[index]

print(find_next_idiom("一言九鼎"))