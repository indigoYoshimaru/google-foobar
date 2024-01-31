def solution(x, y):
    x = int(x)
    y = int(y)
    if x > 10e50 or y > 10e50:
        return "impossible"
    height = 0
    while x > 1 or y > 1:
        if x == y:
            return "impossible"

        mul = 1
        if max(x, y) > min(x, y) * 2:
            mul = (max(x, y) // min(x, y)) - 1
        height += mul
        
        if x > y:
            x -= y * mul
            continue
        if y > x:
            y -= x * mul
            continue
    if x < 0 or y < 0:
        return "impossible"

    return str(height)


def run_with_test_case(func):
    test_cases = [
        ("2", "1"),
        ("4", "7"),
        ("2", "4"),
        ("4", "5"),
        ("3", "4"),
        ("6", "2"),
        ("2", "2"),
        ("3", "10"),
        ("5000", "2"),
        ("1000", "33"),
        ("10000", "1"),
    ]
    results = [
        "1",
        "4",
        "impossible",
        "4",
        "3",
        "impossible",
        "impossible",
        "5",
        "impossible",
        "38",
        "9999",
    ]
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
