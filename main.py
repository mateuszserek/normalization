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

def get_closure(db_func: MultiDict, possible_keys):
    index_of_possible_keys = 0         # atributes closure algorithm
    result = copy(possible_keys)
    db_func_keys = [i for i in db_func]

    while(index_of_possible_keys < len(db_func_keys)):
        index_of_possible_keys = 0
        for key in db_func_keys:
            index_of_possible_keys += 1
            if check_all_in_list(key.split(","), result):
                values = db_func.getall(key)
                for atr in values:
                    if atr not in result:
                        result.append(atr)
                        index_of_possible_keys = 0
    return result

def get_all_closures(db_func: MultiDict, atributes: list):
    closures = []
    atr_combinations = []

    for i in range(1, len(atributes) + 1):
        current = list(itertools.combinations(atributes, i))
        for y in current:
            atr_combinations.append(list(y))

    for possible_keys in atr_combinations:
        current = copy(possible_keys)
        result = get_closure(db_func, current)
        closures.append([sorted(possible_keys),  sorted(result)])

    return closures

def get_different_keys(keys: list, in_key_list: list):
    for key in keys:
        if key not in in_key_list:
            in_key_list.append(key)
       
def get_min_keys_and_print_all_keys(closures, all_atributes):
    min_num = 1
    index_of_first_min = 0
    min_keys = []

    for index, closure in enumerate(closures):
        if closure[1] == all_atributes:
            min_num = len(closure[0])
            index_of_first_min = index
            print(closure[0], " -> ", closure[1], " <-- Minimalny klucz kandydujący") 
            get_different_keys(closure[0], min_keys)
            break
        else:
            print(closure[0], " -> ", closure[1])

    for index, closure in enumerate(closures[index_of_first_min+1:]):
        if closure[1] == all_atributes and len(closure[0]) == min_num:
            print(closure[0], " -> ", closure[1], " <-- Minimalny klucz kandydujący") 
            get_different_keys(closure[0], min_keys)

        elif closure[1] == all_atributes:
            print(closure[0], " -> ", closure[1], " <-- Nadklucz")


        else:
            print(closure[0], " -> ", closure[1])
    
    return sorted(min_keys)

def are_equal_db_func(f_1: MultiDict, f_2: MultiDict):
    f_1_arr = [[key, val] for key, val in f_1.items()]
    f_2_arr = [[key, val] for key, val in f_2.items()]

    for el in f_2_arr:
        el_closure = get_closure(f_1, el[0].split(","))
        if el[1] not in el_closure:
            return False
        
    for el in f_1_arr:
        el_closure = get_closure(f_2, el[0].split(","))
        if el[1] not in el_closure:
            return False 
        
    return True

    
def min_base(f_min: MultiDict):
    func_arr = []
    for key, val in f_min.items():
        func_arr.append([key, val])

    for index, elem in enumerate(func_arr):
        key_atrs = elem[0].split(",")
    
        if len(key_atrs) > 1:
            for f_atr in key_atrs:
                to_check_f = copy(func_arr)
                to_check_f.remove(elem)
                key_str = ""
                for i in key_atrs:
                    if i != f_atr:
                        key_str += f"{i},"
                key_str = key_str[:-1]
                to_check_f.append([key_str, elem[1]])
                if are_equal_db_func(MultiDict(func_arr), MultiDict(to_check_f)):
                    func_arr[index][0] = key_str

    for elem in func_arr:
        cp = copy(func_arr)
        cp.remove(elem)
        if are_equal_db_func(MultiDict(func_arr), MultiDict(cp)):
            func_arr.remove(elem)
    return MultiDict(func_arr)

def is_in_2nf():
    


def main():
    with open("test-01.txt") as f:
        file = f.read().splitlines()
        f = [i for i in file[1:]]
        attrubutes = [i.strip() for i in file[0].split(",")]
        db_functions = parse_functions(f)
        

    all_closures = get_all_closures(db_functions, attrubutes)
    min_keys_atrs = get_min_keys_and_print_all_keys(all_closures, attrubutes)
    not_key_atrs = []

    for i in attrubutes:
        if i not in min_keys_atrs:
            not_key_atrs.append(i)

    print("Atrybuty kluczowe:")

    for i in range(len(min_keys_atrs) - 1):
        print(min_keys_atrs[i], ", ", end = "")

    print(min_keys_atrs[-1])

    print("Atrybuty niekluczowe:")
    if len(not_key_atrs) > 0:
        for i in range(len(not_key_atrs) - 1):
            print(not_key_atrs[i], ", ", end = "")

        print(not_key_atrs[-1])
    else:
        print("Brak")

    f_min = copy(db_functions)

    minimim_base = min_base(f_min)
    print("Baza minimalna:")
    for key, val in minimim_base.items():
        print(key, " -> ", val)

main()