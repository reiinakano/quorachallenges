class TreeNode():
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.children = []
        self.outgoing = []
        self.parent = None
        self.child_number = None
        self.top_outgoing = 0
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def arrange_tree(self):
        s = [self]
        while s:
            current = s.pop()
            for neighbor in current.neighbors:
                if neighbor is not current.parent:
                    s.append(neighbor)
                    current.add(neighbor)

    def add(self, node):
        node.parent = self
        node.child_number = len(self.children)
        self.children.append(node)
        self.outgoing.append(0)

    def __repr__(self):
        display = "Node " + str(self.index)
        for i, node in enumerate(self.children):
            display += "\nChild %d (Node %d): Outgoing=%f" % (i, node.index, self.outgoing[i])
        return display

    def DFS_get_downward_cost(self):
        q1 = [self]
        q2 = []
        while q1:
            popped = q1.pop()
            q2.append(popped)
            for child in popped.children:
                q1.append(child)
        while q2:
            node = q2.pop()
            if not node.parent:
                break
            sum = 0
            for outgoing in node.outgoing:
                sum += outgoing
            sum = sum/float(max(len(node.outgoing), 1))
            sum += node.value
            node.parent.outgoing[node.child_number] = sum

    def DFS_get_incoming_cost(self):
        s = [self]
        while s:
            current = s.pop()
            summed = sum(current.outgoing)
            summed += current.top_outgoing
            for index, child in  enumerate(current.children):
                this_sum = summed - current.outgoing[index]
                if current.top_outgoing == 0:
                    this_sum /= float(max(1, len(current.children) - 1))
                else:
                    this_sum /= float(len(current.children))
                child.top_outgoing = this_sum + current.value
            for child in current.children:
                s.append(child)

    def calculate_self_cost(self):
        num_of_outgoing = len(self.outgoing)
        if self.top_outgoing:
            num_of_outgoing += 1
        if num_of_outgoing:
            return (sum(self.outgoing) + self.top_outgoing)/float(num_of_outgoing) + self.value
        else:
            return self.value

    def calculate_minimum(self):
        s = [self]
        minimum, minimum_node = self.calculate_self_cost(), self
        while s:
            current = s.pop()
            for child in current.children:
                s.append(child)
            if current.calculate_self_cost() < minimum:
                minimum, minimum_node = current.calculate_self_cost(), current

        return minimum_node.index


if __name__ == "__main__":
    N = int(raw_input())
    N_list = map(int, raw_input().split())
    Node_List = []
    for index, value in enumerate(N_list):
        Node_List.append(TreeNode(value,index + 1))
    for i in range(N - 1):
        A, B = map(int, raw_input().split())
        Node_List[A - 1].add_neighbor(Node_List[B - 1])
        Node_List[B - 1].add_neighbor(Node_List[A - 1])

    root = Node_List[N - 1]
    root.arrange_tree()
    root.DFS_get_downward_cost()
    root.DFS_get_incoming_cost()
    print root.calculate_minimum()
