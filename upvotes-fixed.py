array_of_answers = [0] * 100000

def sum_of_first_x_integers(x):
    # return (x*(x+1))>>1
    global array_of_answers
    if array_of_answers[x] == 0:
        array_of_answers[x] = (x*(x+1))>>1
        return array_of_answers[x]
    else:
        return array_of_answers[x]


# This function returns which tuples are within range of the window. For example, if the list is
# [(0,1), (3,6), (8,8)], and (start, end) is (0, 3), the output should be [0,0]
def return_within_range(list, start, end):
    start_index, end_index = None, None
    for index, pair in enumerate(list):
        if pair[1] >= start:
            start_index = index
            break
    if start_index is None:
        return None
    length = len(list)
    index = length - 1
    while index >= 0:
        if list[index][0] <= end:
            end_index = index
            break
        index -= 1
    if end_index < start_index:
        return None
    return (start_index, end_index)


def solve(N, K, Klist):
    previous = Klist[0]
    ascending = []  #  item in list holds a pair of indices that correspond to the start and end of ascending sequence
    descending = []  # item in list holds a pair of indices that correspond to the start and end of descending sequence
    ascending_start = 0
    descending_start = 0
    # build the ascending and descending lists
    for index, current in enumerate(Klist[1:]):
        if current > previous:
            if descending_start < index:
                descending.append((descending_start, index - 1))
            descending_start = index + 1
        elif current < previous:
            if ascending_start < index:
                ascending.append((ascending_start, index - 1))
            ascending_start = index + 1
        previous = current
    if descending_start < N - 1:
        descending.append((descending_start, N - 2))
    if ascending_start < N - 1 :
        ascending.append((ascending_start, N - 2))
    #print ascending
    #print descending
    for start in range(N-K+1):
        end = start + K - 2
        num_of_ascending = 0
        num_of_descending = 0
        indices = return_within_range(ascending, start, end)
        if indices:
            if indices[0] == indices[1]:
                add_to_ascend = min(end, ascending[indices[0]][1]) - max(start, ascending[indices[0]][0]) + 1
                num_of_ascending += sum_of_first_x_integers(add_to_ascend)
            else:
                add_to_ascend = ascending[indices[0]][1] - max(start, ascending[indices[0]][0]) + 1
                num_of_ascending += sum_of_first_x_integers(add_to_ascend)
                add_to_ascend = min(end, ascending[indices[1]][1]) - ascending[indices[1]][0] + 1
                num_of_ascending += sum_of_first_x_integers(add_to_ascend)
                for data in ascending[indices[0] + 1:indices[1]]:
                    num_of_ascending += sum_of_first_x_integers(data[1] - data[0] + 1)
        indices = return_within_range(descending, start, end)
        if indices:
            if indices[0] == indices[1]:
                add_to_descend = min(end, descending[indices[0]][1]) - max(start, descending[indices[0]][0]) + 1
                num_of_descending += sum_of_first_x_integers(add_to_descend)
            else:
                add_to_descend = descending[indices[0]][1] - max(start, descending[indices[0]][0]) + 1
                num_of_descending += sum_of_first_x_integers(add_to_descend)
                add_to_descend = min(end, descending[indices[1]][1]) - descending[indices[1]][0] + 1
                num_of_descending += sum_of_first_x_integers(add_to_descend)
                for data in descending[indices[0] + 1:indices[1]]:
                    num_of_descending += sum_of_first_x_integers(data[1] - data[0] + 1)

        print num_of_ascending - num_of_descending

if __name__ == "__main__":
    N, K = map(int, raw_input().split())
    Klist = map(int, raw_input().split())

    solve(N, K, Klist)