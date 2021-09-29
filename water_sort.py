from copy import deepcopy

def can_pour(x, y):
    if len(y) == 4:
        # print("y is full")
        return False
    if len(x) == 0:
        # print("x is empty")
        return False
    if len(y) != 0 and y[-1] == -1:
        # print("x is unknown")
        return False
    if x[-1] == -1:
        return False
    if len(y) != 0 and x[-1] != y[-1]:
        # print("x does not match y")
        return False
    return True

# Pour x in to y
def pour(x, y):
    while can_pour(x, y):
        y.append(x.pop(-1))
    return (x, y)

def copy_state(state):
    state_copy = deepcopy(state)
    return state_copy

def trim_empty_vials(state):
    c = 0
    for vial in state["vials"]:
        if len(vial) == 0:
            c += 1
    state["empties"] = c
    return state

def vial_is_uniform(vial):

    if len(vial) == 0:
        return False

    return all([vial[i] == vial[0] for i in range(len(vial))])

def get_contiguous_volume(vial):
    c = 1
    for v in range(len(vial)-2, 0, -1):
        # print(v)
        if vial[v] == vial[-1]:
            c += 1
    return c

def vial_is_complete(vial):
    return vial_is_uniform(vial) and len(vial) == 4

def find_complete_vials(vial):
    complete = {}
    for i in range(len(vials)):
        if vial_is_complete(vials[i]):
            complete[vias[i][0]] = i
    return complete

def find_uniform_vials(vials):
    uniform = {}
    for i in range(len(vials)):
        if vial_is_uniform(vials[i]):
            uniform[vials[i][0]] = i
    return uniform

def vial_is_empty(vial):
    return len(vial) == 0

def find_empty_vials(vials):
    empty = []
    for i in range(len(vials)):
        if vial_is_empty(vials[i]):
            empty.append(i)
    return empty

def collect_vial_properties(vials):

    empty = []
    complete = []
    uniform = []
    
    for i in range(len(vials)):
        if vial_is_empty(vials[i]):
            empty.append(i)
        elif vial_is_complete(vials[i]):
            complete.append(i)
        elif vial_is_uniform(vials[i]):
            uniform.append(vials[i])
    
    return {
        "empty": empty,
        "complete": complete,
        "uniform": uniform,
    }

def get_transformations(state):
    transformations = []
    vials = state["vials"]

    # It would be more efficient to combine these loops
    uniform_vials = find_uniform_vials(vials)
    empty_vials = find_empty_vials(vials)

    c = len(vials)
    for i in range(c):

        # Skip i if it is empty
        if i in empty_vials:
            continue

        # If there is a uniform vial available, pour vial i into it
        if vials[i][-1] in uniform_vials.keys():
            target_vial = uniform_vials[vials[i][-1]]
            if target_vial != i:
                # It may not always be valid to do this
                return [(i, uniform_vials[vials[i][-1]])]

        # Otherwise, find all non empty vails i can be poured into
        for j in range(c):
            # Cant pour a vial into itself
            if i == j:
                continue
            # Dont pour into empty vials willy nilly
            if j in empty_vials:
                continue
            # If i can be poured into j, add it as an option
            # TODO: Only add it as an option if the whole of y can be poured into the whole of j
            if can_pour(vials[i], vials[j]):
                # Only add it as an option if the whole of y can be poured into the whole of j
                if get_contiguous_volume(vials[i]) <= (4 - len(vials[j])):
                    transformations.append((i, j))

        # If there is one or more empty vial available, pour i into first available empty vial
        if len(empty_vials) > 0 and i not in uniform_vials.values():
            transformations.append((i, empty_vials[0]))

    return transformations

def pad_state(state):
    for vial in state["vials"]:
        padding = 4 - len(vial)
        for i in range(padding):
            vial.append("_")
    return state

def display_state(state):
    state = copy_state(state)
    state = pad_state(state)

    for i in range(4):
        row = []
        for vial in state["vials"]:
            row.append("{:>2}".format(str(list(reversed(vial))[i])))
        print("  ".join(row))
    print()

def apply_transformation(state, transformation):

    state = copy_state(state)

    v1 = transformation[0]
    v2 = transformation[1]

    vial1 = state["vials"][v1]
    vial2 = state["vials"][v2]
    vial1, vial2 = pour(vial1, vial2)

    state["vials"][v1] = vial1
    state["vials"][v2] = vial2

    state = trim_empty_vials(state)
    state["transformation_history"].append(transformation)
    return state

state_history = []

def foo(state, depth=0, max_depth=5, transformation_history=None):

    # print(depth, "/", max_depth)
    global state_history
    state_history.append(state["vials"])

    if transformation_history is None:
        transformation_history = []

    transformations = get_transformations(state)
    histories[depth] = state

    if depth < max_depth:
        for transformation in transformations:
            next_state = apply_transformation(state, transformation)
            if next_state["vials"] not in state_history:
                foo(
                    next_state,
                    depth=depth+1,
                    max_depth=max_depth,
                )
    else:
        print("Max Depth Reached:", max_depth)
        if len(transformations) > 0:
            histories[depth] = transformation_history

def replay_history(state, history):
    for h in history:
        print("State after applying:", h)
        state = apply_transformation(state, h)
        display_state(state)

state = {
    "vials": [
        [1,2,2,4],
        [6,6,0,7],
        [5,8,0,0],
        [1,7,5,6],
        [7,1,3,4],
        [4,8,5,4],
        [1,3,8,8],
        [7,3,6,3],
        [2,0,2,5],
        [],
        [],
    ],
    "empties": 2,
    "transformation_history": []
}


print("Initial State")
display_state(state)

histories = {}

d=35
foo(state, max_depth=d)
print(histories.keys())
tranformation_history = histories.get(max(histories.keys()))["transformation_history"]
replay_history(state, tranformation_history)
print(len(tranformation_history))

# print(get_contiguous_volume([0,1,1,1]))
