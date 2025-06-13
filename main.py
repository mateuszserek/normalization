from multidict import MultiDict
from copy import copy
import itertools

def parse_functions(db_functions: list) -> MultiDict:
    db_func_dict = MultiDict()

    for i in db_functions:
        splited = i.split("->")

        atrs = splited[1].split(",")
        for atr in atrs:
            db_func_dict.add(splited[0].strip(), atr.strip())

    return db_func_dict

def check_all_in_list(to_check, in_list):
    for i in to_check:
        if i not in in_list:
            return False
    return True

def get_all_closures(db_func: MultiDict, atributes: list):
    closures = []

    atr_combinations = []
    db_func_keys = [i for i in db_func]

    for i in range(1, len(atributes) + 1):
        current = list(itertools.combinations(atributes, i))
        for y in current:
            atr_combinations.append(list(y))

    for i in atr_combinations:
        current = copy(i)
        possible_keys = i

        index_of_possible_keys = 0 # atributes closure algorithm

        while(index_of_possible_keys < len(db_func_keys)):
            index_of_possible_keys = 0
            for key in db_func_keys:
                index_of_possible_keys += 1
                if check_all_in_list(key.split(","), current):
                    values = db_func.getall(key)
                    for atr in values:
                        if atr not in current:
                            current.append(atr)
                            index_of_possible_keys = 0

        closures.append([sorted(possible_keys),  sorted(current)])

    return closures

       
def min_and_over_keys(closures, all_atributes):
    min_num = 1

    for closure in closures:
        if closure[1] == all_atributes:
            print(closure[0], " -> ", closure[1], " <-- Klucz kandydujący") 
        else:
            print(closure[0], " -> ", closure[1])


with open("test-01.txt") as f:
    file = f.read().splitlines()
    f = [i for i in file[1:]]
    attrubutes = [i.strip() for i in file[0].split(",")]
    db_functions = parse_functions(f)
    

all_closures = get_all_closures(db_functions, attrubutes)
min_and_over_keys(all_closures, attrubutes)