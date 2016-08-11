def sum_of_first_x_integers(x):
    return (x*(x+1))>>1

def window_result(K):
    ascending = 0  # non-decreasing. making the name "ascending" is less confusing for me
    descending = 0  # non-increasing
    equal_consecutive = 0
    consecutive = 0
    ascending_flag = False  # True if currently in an ascending phase. False if currently in descending phase. Not valid if "first_change" is True.
    first_change = True  # This flag is to properly handle cases where the sequence starts with current = previous
    previous = K[0]
    for current in K[1:]:
        if first_change:
            if current > previous:
                first_change = False
                ascending_flag = True
                consecutive += 1
                descending += sum_of_first_x_integers(equal_consecutive)
                equal_consecutive = 0
            elif current < previous:
                first_change = False
                ascending_flag = False
                consecutive += 1
                ascending += sum_of_first_x_integers(equal_consecutive)
                equal_consecutive = 0
            else: # if equal
                consecutive += 1
                equal_consecutive += 1
        else:
            if current > previous:
                if ascending_flag:
                    consecutive += 1
                    descending += sum_of_first_x_integers(equal_consecutive)
                    equal_consecutive = 0
                else:
                    ascending_flag = True
                    descending += sum_of_first_x_integers(consecutive)
                    consecutive = 1
                    consecutive += equal_consecutive
                    equal_consecutive = 0
            elif current < previous:
                if not ascending_flag:
                    consecutive += 1
                    ascending += sum_of_first_x_integers(equal_consecutive)
                    equal_consecutive = 0
                else:
                    ascending_flag = False
                    ascending += sum_of_first_x_integers(consecutive)
                    consecutive = 1
                    consecutive += equal_consecutive
                    equal_consecutive = 0
            else: # if equal
                consecutive += 1
                equal_consecutive += 1
        previous = current
    if first_change: # did not change at all
        return 0
    else:
        if ascending_flag:
            ascending += sum_of_first_x_integers(consecutive)
            descending += sum_of_first_x_integers(equal_consecutive)
        else:
            descending += sum_of_first_x_integers(consecutive)
            ascending += sum_of_first_x_integers(equal_consecutive)
        return ascending - descending

if __name__ == "__main__":
    N, K = map(int, raw_input().split())
    Klist = map(int, raw_input().split())
    for i in range(N - K + 1):
        print window_result(Klist[i:i+K])