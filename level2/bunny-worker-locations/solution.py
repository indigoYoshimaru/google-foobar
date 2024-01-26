def solution(x, y):
    n = x + (y - 2)
    return (n * (n + 1) / 2) + x


def run_with_test_case(func):
    test_cases = [(1, 1), (3, 2), (5, 10)]
    results = [1, 9, 96]
    try:
        for idx, test_case in enumerate(test_cases):
            output = func(*test_case)
            assert (
                output == results[idx]
            ), f"Expected {results[idx]} but found {output} for test case {test_case}"

    except Exception as e:
        raise e
    else:
        print("You passed")


run_with_test_case(solution)