
def solution(pegs):
    import numpy as np
    from decimal import Decimal
    from fractions import Fraction
    
    pegs = list(filter(lambda x: pegs.count(x)==1, pegs))
    
    if len(pegs)<2 or len(pegs)>20:
        return (-1, -1)
    if len(pegs)==2: 
        res =  Fraction((pegs[-1]-pegs[0])*2/3).limit_denominator(10000)
        if res.numerator<res.denominator:
            return (-1, -1)
        return (res.numerator, res.denominator)

    la_matrix = []
    pegs_diff = []
    for i in range(0, len(pegs) - 1):
        diff = abs(pegs[i + 1] - pegs[i])
        pegs_diff.append(diff)
        row = [0] * i + [1] * 2 + [0] * (len(pegs) - 3 - i)
        if i == len(pegs) - 2:
            row = [0.5] + [0] * (i - 1) + [1]
        la_matrix.append(row)
    
    try:
        res_mtx = np.matmul(
            np.linalg.inv(np.array(la_matrix)),
            np.array(pegs_diff),
        ).tolist()
    except: 
        return (-1, -1)
    
    for res in res_mtx:
        if res<1:
            return (-1, -1)

    res =  Fraction(Decimal(res_mtx[0])).limit_denominator(10000)
    return (res.numerator, res.denominator)


def run_with_test_case(func):
    test_cases = [
        [4, 17, 50],
        [4, 30, 50],
    ]
    results = [
        (-1, -1),
        (12, 1)
    ]
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
