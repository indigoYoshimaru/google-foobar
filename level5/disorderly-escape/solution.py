from collections import Counter

def solution(w, h, s): 
    symm_count = 0
    for part_w in partitions(w): 
        for part_h in partitions(h): 
            cycle_count = count(part_w, w)*count(part_h, h)
            symm_count += cycle_count*(s**find_gcd(part_w, part_h))
    return str(symm_count//(factorial(w)*factorial(h)))

def find_gcd(pw, ph): 
    gcd_sum = 0
    for i in pw:
        for j in ph: 
            gcd_sum+= gcd(i, j)
    return gcd_sum

def count(c, n):
    cnt=factorial(n)
    for a, b in Counter(c).items():
        cnt//=(a**b)*factorial(b)
    return cnt 

def partitions(n, i=1):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[: k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[: k + 1]

def gcd(x,y):
    while y:
        x,y=y,x%y
    return x

def factorial(n):
    if n==0:
        return 1

    return n*factorial(n-1)

def run_with_test_case(func):
    test_cases = [
        (2, 2, 2),
        (2, 3, 4),
    ]
    results = ['7', '430']
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