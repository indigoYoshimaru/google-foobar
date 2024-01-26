def solution(data, n): 
    if not data or not n: 
        return []
    return list(filter(lambda x: data.count(x)<=n, data))


def run_with_test_case(func):
    test_cases = [
        ([5, 10, 15, 10, 7], 1),
        ([1, 2, 3], 0),
        ([1, 2, 2, 3, 3, 3, 4, 5, 5], 1),
    ]
    results = [
        [5, 15, 7],
        [],
        [1, 4],
    ]
    try:
        for idx, test_case in enumerate(test_cases):
            output = func(test_case[0], test_case[1])
            assert (
                output == results[idx]
            ), f"Expected {results[idx]} but found {output} for test case {test_case}"

    except Exception as e:
        raise e
    else:
        print("You passed")

run_with_test_case(solution)