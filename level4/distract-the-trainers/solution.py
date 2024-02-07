import math
def is_pair(min_val, max_val, sum_val, min_list): 
    # print(f'{min_val=}-{max_val=}-{sum_val=}-{min_list}')
    if sum_val%2!=0: 
        return True
    if min_val in min_list: 
        return True
    mid_val = sum_val/2
    if min_val == mid_val: 
        return False
    
    min_list.append(min_val)
    k = math.ceil(math.log2((max_val-mid_val)/float(min_val)+1))+1
    new_vals = [
        max_val - (2**(k-1)-1)*min_val,
        min_val + (2**(k-1)-1)*min_val,
    ]
    min_val = min(new_vals)
    max_val = max(new_vals)
    # print(f'{k=}-{new_vals=}')
    return is_pair(min_val, max_val, sum(new_vals), min_list)

# def to_str(i, j):
#     return f'[{i},{j}]'

# def find_sum(trainer_pair): 
    # visited = dict()
    # best_sum = 0
    # cur_sum = 0
    # for pair, is_pair in trainer_pair.items(): 
    #     # if not is_pair: 
    #     #     continue
    #     u, v = eval(pair)
    #     if u not in visited and v not in visited: 
    #         visited.append(u)
    #         visited.append(v)
    #         print(u, v)
    #         cur_sum +=is_pair
    #         best_sum = max(best_sum, cur_sum)
    #         print(f"{best_sum=}-{cur_sum=}")
    #     else: 
    #         cur_sum +=is_pair
    #         best_sum = max(best_sum, cur_sum)
    #         print(f'in visited: {u}, {v}')
    #         print(f"{best_sum=}-{cur_sum=}")
    #     # print(visited)

    # for pair, is_pair in trainer_pair.items(): 
    #     if not is_pair: 
    #         continue
    #     u, v = eval(pair)
    #     if u not in visited: 
    #         visited[u] = [v]
    #         print(visited) 
    #     else:  
    #         visited[u].append(v) 
                
    # print(visited)
    # visited = dict((k, v) for k, v in visited.items() if v)
    # print(visited)
        

def solution(banana_list):
    if len(banana_list)<1 or len(banana_list)>100:
        return len(banana_list)
    trainer_pair = dict()
    visited = []
    for i, trainer in enumerate(banana_list): 
        for j in range(i+1, len(banana_list)): 
            val = int(is_pair(min(trainer, banana_list[j]), max(trainer, banana_list[j]), trainer+ banana_list[j], []))
            if val: 
                # trainer_pair[to_str(trainer, banana_list[j])] = val
                visited.append(trainer)
                visited.append(banana_list[j])
                # trainer_pair[to_str(banana_list[j], trainer)] = val
    res = list(filter(lambda x: x not in visited, banana_list))
    print(visited)
    # find_sum(trainer_pair)
    return len(res)

def run_with_test_case(func, stop_when_fail: bool = True):
    from colorama import Fore
    from colorama import init as colorama_init

    colorama_init(autoreset=True)

    test_cases = [
       [1, 1], 
    #    [1,4,3,5],
       [1, 7, 3, 21, 13, 19],
    ]

    results = [
        2,
        # 1,
        0,

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