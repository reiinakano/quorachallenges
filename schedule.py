if __name__ == "__main__":
    N = int(raw_input())
    tests = []
    for i in range(N):
        tests.append(map(float, raw_input().split()))
    #print tests
    for row in tests:
        row.append(row[0]*row[1])
    #print tests
    tests.sort(key=lambda x: x[1])
    #print tests
    dummy = 0
    for row in tests:
        row[0] += dummy
        dummy = row[0]
    #print tests
    what_is_left = 1.0
    sum = 0.0
    for i, row in enumerate(tests):
        if i == N - 1:
            row.append(row[0]*what_is_left)
            sum += row[3]
        else:
            row.append(row[0]*what_is_left*(1 - row[1]))
            what_is_left = what_is_left*(row[1])
            sum += row[3]
    #print tests
    print sum