import numpy as np

class Position:
    def __init__(self, position, original_pos, role):
        self.position = np.asarray(position)
        original_pos = np.array(original_pos)    
        
        u = position-original_pos
        self.distance = np.linalg.norm(u)
        self.angle = np.arctan2(u[1], u[0])
        self.role = role

    def __str__(self) -> str:
        return f'position: {self.position} - distance: {self.distance} - angle: {self.angle} - role: {self.role}'
    
def check_cond(arr, min_bound, max_bound):
    arr = np.asarray(arr)
    min_bound = np.asarray(min_bound)
    max_bound = np.asarray(max_bound)
    return (arr - min_bound).all() * (max_bound - arr).all()

def project_x(pos, original_pos, dim, x):
    right, left = [], []
    positive_proj_pos = pos.position
    negative_proj_pos = pos.position
    for i in range(1,x+2):
        positive_proj_pos = [2*i*dim[0] - positive_proj_pos[0], positive_proj_pos[1]]
        negative_proj_pos = [-2*(i-1)*dim[0] - negative_proj_pos[0], negative_proj_pos[1]]
        
        right.append(Position(positive_proj_pos, original_pos, role = pos.role))
        left.append(Position(negative_proj_pos, original_pos, role = pos.role))
    return right + left


def project_y(pos, original_pos, dim, y, role):
    top, bottom = [Position(pos, original_pos, role)], []
    positive_proj_pos = pos
    negative_proj_pos = pos
    # project top and bottom wall
    for i in range(1, y+2):
        positive_proj_pos = [positive_proj_pos[0], 2*i*dim[1] - positive_proj_pos[1]]
        negative_proj_pos = [negative_proj_pos[0], -2*(i-1)*dim[1]- negative_proj_pos[1]]
        top.append(Position(positive_proj_pos, original_pos, role))
        bottom.append(Position(negative_proj_pos, original_pos, role))
    return top + bottom

def solution(dimensions, your_position, guard_position, distance): 
    try:
        condition = check_cond(
            dimensions + your_position + guard_position + [distance],
            [1, 1] + [0, 0] + [0, 0] + [1],
            [1251, 1251] + dimensions + dimensions + [10001],
        )
        assert condition, "Invalid condition"
    except AssertionError as e:
        return 0
    
    from math import ceil
    x_project = int(ceil((your_position[0] + distance) / float(dimensions[0])))
    y_project = int(ceil((your_position[1] + distance) / float(dimensions[1])))

    your_y_projection = project_y(your_position, your_position, dimensions, y_project, role='you')
    guard_y_projection = project_y(guard_position, your_position, dimensions, y_project, role = 'guard')
    
    projections = []
    
    for i in range(len(your_y_projection)):
        projections += project_x(your_y_projection[i], your_position, dimensions, x_project)
        projections += project_x(guard_y_projection[i], your_position, dimensions, x_project)
    projections += your_y_projection+guard_y_projection
    
    project_dict = dict()
    for proj in projections: 
        if proj.angle not in project_dict:
            if  proj.distance>distance or proj.distance<=0:
                continue 
            project_dict[proj.angle] = proj
            continue
        if distance>=project_dict[proj.angle].distance>proj.distance>0: 
            project_dict[proj.angle] = proj
            continue

    positions = list(project_dict.values())
    positions = list(filter(lambda x: x.role=='guard', positions))

    return len(positions)

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
        # [[10, 10], [4, 4], [3, 3], 5000],
        [[3, 2], [1, 1], [2, 1], 7],
        [[2, 3], [1, 1], [1, 2], 4],
        [[3, 4], [1, 2], [2, 1], 7],
        [[4, 4], [2, 2], [3, 1], 6],
        [[300, 275], [150, 150], [180, 100], 500],
        # [[3, 4], [1, 1], [2, 2], 500],
        [[1000, 1000], [250, 25], [257, 49], 25],
    ]

    results = [7, 9, 27, 8, 196, 
            #    739323, 
            19, 7, 10, 7, 9, 
            # 54243, 
            1, ]

    try:
        for idx, test_case in enumerate(test_cases):
            output = func(*test_case)
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
