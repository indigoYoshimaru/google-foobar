def find_xor(n):
    # this is the pattern of xor, using reduce for the whole range will not pass test cases with larger number!
    n -= 1
    mod = n % 4
    if mod == 0:
        return n
    if mod == 2:
        return n + 1
    if mod == 3:
        return 0
    return mod


def solution(start, length):
    max_id = 2000000000
    end = start + length**2
    # check for condition
    if length < 1 or start > max_id or end > max_id or start < 0:
        return None
    checksum = 0

    for i in range(length, 0, -1):
        checksum ^= find_xor(start) ^ find_xor(start + i)
        start += length
    return checksum


def run_with_test_case(func):
    test_cases = [
        (0, 3),
        (17, 4),
    ]
    results = [2, 14]
    try:
        for idx, test_case in enumerate(test_cases):
            output = func(*test_case)
            print(f"{output=}")
            assert (
                output == results[idx]
            ), f"Expected {results[idx]} but found {output} for test case {test_case}"

    except Exception as e:
        raise e
    else:
        print("You passed")


run_with_test_case(solution)
