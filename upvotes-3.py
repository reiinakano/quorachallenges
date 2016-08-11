def generate_ranges(Klist):
    length = len(Klist)
    increasing_left_side = range(length)
    increasing_right_side = range(length)
    decreasing_left_side = range(length)
    decreasing_right_side = range(length)
    index = 1
    while index < length:
        reverse_index = length - 1 - index
        if Klist[index] >= Klist[index - 1]:
            increasing_left_side[index] = increasing_left_side[index - 1]
        if Klist[index] <= Klist[index - 1]:
            decreasing_left_side[index] = decreasing_left_side[index - 1]
        if Klist[reverse_index + 1] >= Klist[reverse_index]:
            increasing_right_side[reverse_index] = increasing_right_side[reverse_index + 1]
        if Klist[reverse_index + 1] <= Klist[reverse_index]:
            decreasing_right_side[reverse_index] = decreasing_right_side[reverse_index + 1]
        index += 1
    return increasing_left_side, increasing_right_side, decreasing_left_side, decreasing_right_side

if __name__ =="__main__":
    N, K = map(int, raw_input().split())
    Klist = map(int, raw_input().split())
    #N = 10
    #K = 4
    #Klist = [2, 2, 3, 4, 5, 5, 5, 4, 4, 4]
    increasing_left_side, increasing_right_side, decreasing_left_side, decreasing_right_side = generate_ranges(Klist)
    #print increasing_left_side
    #print increasing_right_side
    #print decreasing_left_side
    #Sprint decreasing_right_side
    initial_value = 0
    for i in range(K):
        initial_value += min(increasing_right_side[i], K - 1) - i
        initial_value -= min(decreasing_right_side[i], K - 1) - i
    print initial_value
    for i in range(N - K):
        end = K + i
        initial_value -= min(increasing_right_side[i], end) - i  # remove whatever was removed
        initial_value += min(decreasing_right_side[i], end) - i
        initial_value += end - max(i, increasing_left_side[end])
        initial_value -= end - max(i, decreasing_left_side[end])
        print initial_value