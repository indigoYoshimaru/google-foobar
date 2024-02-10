# my terrible mistake
# def is_pair(min_val, max_val, val_list): 
#     print(f'{min_val=}-{max_val=}-{val_list}')
#     if (min_val+max_val)%2: 
#         return True
#     if min_val in val_list: 
#         return True
#     mid_val = (min_val+max_val)/2
#     if min_val == mid_val: 
#         return False
    
#     val_list.append(min_val)
#     k = max(math.ceil(math.log((max_val-mid_val)/float(min_val)+1))+1,1)
#     new_vals = [
#         max_val - (2**(k-1)-1)*min_val,
#         min_val + (2**(k-1)-1)*min_val,
#     ]
#     min_val = min(new_vals)
#     max_val = max(new_vals)
#     # print(f'{k=}-{new_vals=}')
#     return is_pair(min_val, max_val, val_list)
 

def is_pair(x, y):
    n_tilde = x+y
    while n_tilde % 2 == 0:
        n_tilde /= 2
    return (x % n_tilde) != 0


def bpm(banana_list, u, bunny_match, visited): 
    for v in range(len(banana_list)):
        if is_pair(banana_list[u],banana_list[v]) and not visited[v]:
                
            visited[v] = True
            if bunny_match[v] == -1 or bpm(banana_list, bunny_match[v], 
                                            bunny_match, visited):
                bunny_match[v] = u
                return True
            
    return False

def solution(banana_list):
    if len(banana_list)<=1 or len(banana_list)>100:
        return len(banana_list)
    banana_list = sorted(banana_list)
    if banana_list[-1]>2**30:
        return len(banana_list)

    bunny_match = [-1] * len(banana_list)
    result = 0
    for trainer_i in range(len(banana_list)):
        visited = [False] * len(banana_list)  
        if bpm(banana_list, trainer_i, bunny_match, visited):
            result += 1
    return len(banana_list) - 2*(result/2)


def run_with_test_case(func, stop_when_fail: bool = True):
    from colorama import Fore
    from colorama import init as colorama_init

    colorama_init(autoreset=True)

    test_cases = [
       [1, 1], 
       [1,4,3,5],
       [1, 7, 3, 21, 13, 19],
       [1,1,1,2],
       [1,7,3,3],
       [3,7,3,7],
       [3,7,3,7,3],
       [1]
    ]

    results = [
        2,
        0,
        0,
        2, 
        2,
        0,
        1,
        1,
    ]

    try:
        for idx, test_case in enumerate(test_cases):
            output = func(test_case)
            if stop_when_fail:
                assert (
                    output == results[idx]
                ), f"Expected {results[idx]} but found {output} for test case {test_case}"
            if output != results[idx]:
                print(
                    f"{Fore.RED}Expected {results[idx]} but found {output} for test case {test_case}"
                )
                continue
            print(f"{Fore.GREEN}Passed. {output=}")
    except Exception as e:
        print(f"{Fore.RED}{e}")
        raise e
    else:
        print(f"{Fore.GREEN}Passed all test cases")

run_with_test_case(solution)