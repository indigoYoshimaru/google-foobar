import numpy as np

sin_dict = dict()

def check_cond(arr, min_bound, max_bound):
    arr = np.asarray(arr)
    min_bound = np.asarray(min_bound)
    max_bound = np.asarray(max_bound)
    return (arr - min_bound).all() * (max_bound - arr).all()


def project_x(pos, dim, x):
    right, left = [], []
    positive_proj_pos = pos
    negative_proj_pos = pos
    for i in range(1,x+2):
        positive_proj_pos = [2*i*dim[0] - positive_proj_pos[0], positive_proj_pos[1]]
        negative_proj_pos = [-2*(i-1)*dim[0] - negative_proj_pos[0], negative_proj_pos[1]]
        right.append(positive_proj_pos)
        left.append(negative_proj_pos)
    return right + left


def project_y(pos, dim, y):
    top, bottom = [pos], []
    positive_proj_pos = pos
    negative_proj_pos = pos
    # project top and bottom wall
    for i in range(1, y+2):
        positive_proj_pos = [positive_proj_pos[0], 2*i*dim[1] - positive_proj_pos[1]]
        negative_proj_pos = [negative_proj_pos[0], -2*(i-1)*dim[1]- negative_proj_pos[1]]
        top.append(positive_proj_pos)
        bottom.append(negative_proj_pos)
    return top + bottom
    

def filter_position(positions_distance_tuple):
    positions, your_pos, dimensions, distance = positions_distance_tuple
    your_pos = np.asarray(your_pos)
    your_proj_pos = np.asarray(positions[0])
    guard_proj_pos = np.asarray(positions[1])

    shoot_distance = np.linalg.norm(guard_proj_pos - your_pos)
    proj_distance = np.linalg.norm(your_proj_pos - your_pos)
    # print(guard_proj_pos)
    # print(f"{shoot_distance=} - {proj_distance=}")
    # filter distance
    if  shoot_distance > distance >0:
        # print(f'distance: {guard_proj_pos}')
        return False

    # check if shoot vector is linear dep with project vector
    det = np.linalg.det([guard_proj_pos - your_proj_pos, your_proj_pos - your_pos])
    # print(f"{det=}-{(your_proj_pos-your_pos)=}")
    if not det and shoot_distance>proj_distance>0:
        # print(f"det: {guard_proj_pos}")
        return False
    # check if shoot vector meets the corner
    # for x in [[0, 0], [0, dimensions[1]], [dimensions[0], 0], dimensions]:
    #     if not np.linalg.det([guard_proj_pos - your_pos, np.asarray(x) - your_pos]):
    #         print(f'corner: {guard_proj_pos}')
    #         return False
    # sin_guard_pos = np.linalg.norm(guard_proj_pos- your_pos)/np.linalg.norm(your_pos)
    global sin_dict
    # print(sin_dict)
    u = guard_proj_pos-your_pos
    from math import atan2
    sin_guard_pos = atan2(u[1], u[0])
    # sin_guard_pos = np.arccos(np.clip(np.dot(u,your_pos)/np.linalg.norm(u)/np.linalg.norm(your_pos), -1, 1))
    # if shoot_distance>sin_dict.get(sin_guard_pos, [10000, []])[0]:
    # print(f"distance_angle: {guard_proj_pos=} - {shoot_distance} -  {sin_guard_pos=}")
    if sin_guard_pos not in sin_dict:
        sin_dict[sin_guard_pos] = [shoot_distance, guard_proj_pos]
        return True

    if sin_guard_pos in sin_dict and shoot_distance>=sin_dict.get(sin_guard_pos, [10000, []])[0]:
        # print(f"{guard_proj_pos=} - {sin_dict.get(sin_guard_pos)=} - {sin_guard_pos=} - {shoot_distance}")
        return False
    
    sin_dict[sin_guard_pos] = [shoot_distance, guard_proj_pos]
    print(f'{sin_dict}')
    return True
    
def solution(dimensions, your_position, guard_position, distance):
    # check conditions
    from math import ceil

    try:
        condition = check_cond(
            dimensions + your_position + guard_position + [distance],
            [1, 1] + [0, 0] + [0, 0] + [1],
            [1251, 1251] + dimensions + dimensions + [10001],
        )
        assert condition, "Invalid condition"
    except AssertionError as e:
        return 0
    # find number of projection to make
    x_project = int(ceil((your_position[0] + distance) / float(dimensions[0])))
    y_project = int(ceil((your_position[1] + distance) / float(dimensions[1])))
    your_y_projection = project_y(your_position, dimensions, y_project)
    guard_y_projection = project_y(guard_position, dimensions, y_project)
    # print(list(zip(your_y_projection, guard_y_projection)))
    your_projection = []
    guard_projection = []
    for i in range(len(your_y_projection)):
        your_projection += project_x(your_y_projection[i], dimensions, x_project)
        guard_projection += project_x(guard_y_projection[i], dimensions, x_project)
    your_projection += your_y_projection
    guard_projection += guard_y_projection
    # print(f'{list(zip(your_projection, guard_projection))}')

    # remove duplicated position
    filtered_positions = []
    for positions in zip(your_projection, guard_projection):
        if (positions, your_position, dimensions, distance) not in filtered_positions:
            filtered_positions.append((positions, your_position, dimensions, distance))
    # print(len(filtered_positions))

    # filter positions by trajectory and distance    
    filtered_positions = list(filter(filter_position, filtered_positions))
    # print(f"{len(filtered_positions)=}")
    print('my_guard_pos=[')
    for pos in sin_dict.values():
        print(f'{pos[1]},')
    print(']')
    return len(sin_dict)

def run_with_test_case(func, stop_when_fail: bool = True):
    from colorama import Fore
    from colorama import init as colorama_init

    colorama_init(autoreset=True)

    test_cases = [
        [[3, 2], [1, 1], [2, 1], 4],
        [[300, 275], [150, 150], [185, 100], 500],
        [[2, 5], [1, 2], [1, 4], 11],
        [[23, 10], [6, 4], [3, 2], 23],
        [[1250, 1250], [1000, 1000], [500, 400], 10000],
        [[10, 10], [4, 4], [3, 3], 5000],
        [[3, 2], [1, 1], [2, 1], 7],
        [[2, 3], [1, 1], [1, 2], 4],
        [[3, 4], [1, 2], [2, 1], 7],
        [[4, 4], [2, 2], [3, 1], 6],
        [[300, 275], [150, 150], [180, 100], 500],
        [[3, 4], [1, 1], [2, 2], 500],
        [[1000, 1000], [250, 25], [257, 49], 25],
    ]

    results = [7, 9, 27, 8, 196, 739323, 19, 7, 10, 7, 9, 54243, 1,]

    try:
        for idx, test_case in enumerate(test_cases):
            output = func(*test_case)
            global sin_dict
            sin_dict =dict()
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
        print(f"{Fore.GREEN}Passed all test case {output=}")


run_with_test_case(solution)
