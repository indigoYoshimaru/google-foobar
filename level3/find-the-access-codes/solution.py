def solution(l):
    if len(l) < 3:
        return 0

    divisors = {k: 0 for k in range(len(l))}
    counter = 0
    for i in range(1, len(l)):
        for j in range(i):
            if l[i] % l[j] == 0:
                divisors[i] += 1 
                counter += divisors[j]
    return counter


def run_with_test_case(func):
    test_cases = [[1, 1, 1], [1, 2, 3, 4, 5, 6], [1]]
    results = [1, 3, 0]
    try:
        for idx, test_case in enumerate(test_cases):
            output = func(test_case)
            print(f"{output=}")
            assert (
                output == results[idx]
            ), f"Expected {results[idx]} but found {output} for test case {test_case}"

    except Exception as e:
        raise e
    else:
        print("You passed")


run_with_test_case(solution)
