from multidict import MultiDict
import itertools

def parse_functions(db_functions: list) -> MultiDict:
    db_func_dict = MultiDict()

    for i in db_functions:
        splited = i.split("->")
        db_func_dict.add(splited[0].strip(), splited[1].strip())

    return db_func_dict

def check_all_in_list(to_check, in_list):
    for i in to_check:
        if i not in in_list:
            return False
    return True

def closure(db_func: MultiDict, atributes: list):
    closures = dict()
    atr_combinations = []

    db_func_keys = [i for i in db_func]

    for i in range(len(atributes), 0, -1):
        current = list(itertools.combinations(atributes, i))
        for y in current:
            atr_combinations.append(list(y))

    for i in atr_combinations:
        current = [p for p in i]
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


        print(possible_keys, "->", current)

       

with open("test-01.txt") as f:
    file = f.read().splitlines()
    f = [i for i in file[1:]]
    attrubutes = [i.strip() for i in file[0].split(",")]
    db_functions = parse_functions(f)
    

closure(db_functions, attrubutes)


