import bisect


if __name__ == "__main__":
    N = int(raw_input())
    circles = map(int, raw_input().split())
    circles = [radius*radius for radius in circles]  # Is it sorted?
    circles = sorted(circles)
    #print circles
    M = int(raw_input())
    total_Q = 0
    for i in range(M):
        coordinates = map(int, raw_input().split())
        point_A = coordinates[0]*coordinates[0] + coordinates[1]*coordinates[1]
        point_B = coordinates[2]*coordinates[2] + coordinates[3]*coordinates[3]
        #print point_A, point_B
        point_A, point_B = bisect.bisect_left(circles, point_A), bisect.bisect_left(circles, point_B)
        #print point_A, point_B
        total_Q += abs(point_A - point_B)
    print total_Q
