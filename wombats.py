from collections import deque

class VertexWeightedGraph():
    def __init__(self, graph):
        self.graph = graph

    def convert_to_flow_graph(self):
        flow_graph = {"src":[], "sink":[]}
        for key, value in self.graph.iteritems():
            flow_graph[key] = [[neighbor, float("inf")] for neighbor in value[1]]
            if value[0] > 0:
                flow_graph["src"].append([key, value[0]])
            if value[0] < 0:
                flow_graph[key].append(["sink", -value[0]])
        return flow_graph

    def __repr__(self):
        return str(sorted(self.graph.iteritems()))

    def getMaxClosure(self):
        flow_graph = FlowGraph(self.convert_to_flow_graph())
        flow_graph.get_residual_graph()
        nodes = flow_graph.find_accessible_nodes()
        max_closure = 0
        for key in nodes:
            if key != "src":
                max_closure += self.graph[key][0]
        return max_closure


class FlowGraph():
    def __init__(self, graph):
        self.graph = graph
        self.residual_graph = None

    def find_shortest(self, src, dst):  # find shortest path between src to dst using BFS in self.graph
        previous_node = {}
        visited = {}
        q = deque()
        q.append(src)
        current_node = src
        previous_node[src] = None
        while q:
            current_node = q.popleft()
            if current_node == dst:
                break
            for neighbor in self.graph[current_node]:
                if neighbor[0] not in previous_node:
                    q.append(neighbor[0])
                    previous_node[neighbor[0]] = current_node
        if current_node != dst:
            return None
        else:
            reverse_path = []
            while current_node in previous_node:
                reverse_path.append(current_node)
                current_node = previous_node[current_node]
            return reverse_path

    def find_shortest_residual(self):  # find shortest path between source and sink in self.residual_graph
        previous_node = {}
        q = deque()
        q.append("src")
        current_node = "src"
        previous_node["src"] = None, None  # this dict contains for each key a tuple of (previous node, previous edge)
        while q:
            current_node = q.popleft()
            if current_node == "sink":
                break
            for edge in self.residual_graph[current_node]:
                if edge.src == current_node and edge.capacity > edge.current_flow and edge.dst not in previous_node:
                    q.append(edge.dst)
                    previous_node[edge.dst] = current_node, edge
                elif current_node == edge.dst and edge.current_flow > 0 and edge.src not in previous_node:
                    q.append(edge.src)
                    previous_node[edge.src] = current_node, edge
        if current_node != "sink":
            return None
        else:
            reverse_path = []
            while current_node != "src":
                reverse_path.append(previous_node[current_node])
                current_node = previous_node[current_node][0]
            return reverse_path

    def update_path(self, path):  # use only for the return value in find_shortest_residual
        if path is None:
            return
        flow_max_values = []
        for flow in path:
            if flow[0] == flow[1].src:
                flow_max_values.append(flow[1].capacity - flow[1].current_flow)
            else:
                flow_max_values.append(flow[1].current_flow)
        possible_flow = min(flow_max_values)
        for flow in path:
            if flow[0] == flow[1].src:
                flow[1].current_flow += possible_flow
            else:
                flow[1].current_flow -= possible_flow
        #print possible_flow
        #print path

    def edmond_karp(self):  # use edmond karp to find max flow. only use after calling get_residual_graph
        if not self.residual_graph:
            raise AssertionError
        path = 1  # default value
        while path:
            path = self.find_shortest_residual()
            self.update_path(path)
        max_flow = 0
        print self.residual_graph["src"]
        for edge in self.residual_graph["src"]:
            if edge.src == "src":
                max_flow += edge.current_flow
        return max_flow

    def find_accessible_nodes(self): # uses EK and finds accessible nodes
        if not self.residual_graph:
            raise AssertionError
        path = 1
        while path:
            path = self.find_shortest_residual()
            self.update_path(path)
        visited = {"src":True}
        q = deque()
        q.append("src")
        while q:
            current_node = q.popleft()
            if current_node == "sink":
                break
            for edge in self.residual_graph[current_node]:
                if edge.src == current_node and edge.capacity > edge.current_flow and edge.dst not in visited:
                    q.append(edge.dst)
                    visited[edge.dst] = True
                elif current_node == edge.dst and edge.current_flow > 0 and edge.src not in visited:
                    q.append(edge.src)
                    visited[edge.src] = True
        return visited


    def get_residual_graph(self):  # updates self.residual with full capacity (and using Edge class) using self.graph
        residual = {}
        for key, value in self.graph.iteritems():
            to_add = [Edge(key, pair[0], pair[1]) for pair in value]
            residual[key] = to_add
        for key in residual:
            for edge in residual[key]:
                if edge.src == key:
                    residual[edge.dst].append(edge)
        self.residual_graph = residual


class Edge():
    def __init__(self, src, dst, capacity):
        self.capacity = capacity
        self.current_flow = 0
        self.src = src
        self.dst = dst

    def __repr__(self):
        return "|||Edge (%s)-->(%s): C=%.1f, CF=%d|||" %(self.src, self.dst, self.capacity, self.current_flow)


def create_graph(triangles):  # creates graph from triangles array
    graph = {}
    N = len(triangles)
    for i in range(N):
        if i == 0:
            graph["%d,%d,%d" %(i, i, i)] = triangles[0][0][0], []
        else:
            for j, row in enumerate(triangles[i]):
                for k, member in enumerate(row):
                    graph["%d,%d,%d" %(i, j, k)] = member, []
                    if "%d,%d,%d" %(i - 1, j, k) in graph:
                        graph["%d,%d,%d" %(i, j, k)][1].append("%d,%d,%d" %(i - 1, j, k))
                    if "%d,%d,%d" %(i - 1, j-1, k) in graph:
                        graph["%d,%d,%d" %(i, j, k)][1].append("%d,%d,%d" %(i - 1, j-1, k))
                    if "%d,%d,%d" %(i - 1, j, k-1) in graph:
                        graph["%d,%d,%d" %(i, j, k)][1].append("%d,%d,%d" %(i - 1, j, k-1))
    return graph


if __name__ == "__main__":
    triangles = []
    N = int(raw_input())
    for num in range(N):  # build the triangular layers of the pyramid
        triangles.append([])
    for i, triangle in enumerate(triangles):
        for x in range(i + 1):  # build the layers in each triangle
            triangle.append([])
        for x in range(i + 1):  # fill up each row in the triangle
            row = map(int, raw_input().split())
            for value in row:
                triangle[x].append(value)
    graph = VertexWeightedGraph(create_graph(triangles))
    #print graph
    #flow_graph = graph.convert_to_flow_graph()
    #print sorted(flow_graph.iteritems())
    #flow_graph = FlowGraph(flow_graph)
    #print flow_graph.find_shortest("src", "sink")
    #flow_graph.get_residual_graph()
    #print sorted(flow_graph.residual_graph.iteritems())

    #print flow_graph.edmond_karp()

    #print flow_graph.find_accessible_nodes()
    print graph.getMaxClosure()
