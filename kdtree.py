class EmptyKDNode:
    def insert(self, new_data):
        return KDNode(new_data)

    def exists(self, query, tolerance=0):
        return False

empty = EmptyKDNode()

class KDNode:
    def __init__(self, data, axis=0, left=empty, right=empty):
        self.data = data
        self.axis = axis
        self.left = left
        self.right = right

    def insert(self, new_data):
        self.check_dimensionality(new_data)

        if new_data[self.axis] < self.data[self.axis]:
            new_left = self.left.insert(new_data)
            new_left.axis = (self.axis + 1) % len(self.data)
            return KDNode(self.data, self.axis, new_left, self.right)
        else:
            new_right = self.right.insert(new_data)
            new_right.axis = (self.axis + 1) % len(self.data)
            return KDNode(self.data, self.axis, self.left, new_right)

    def exists(self, query, tolerance=0):
        self.check_dimensionality(query)
        distance = self.get_distance(query)
        
        if distance <= tolerance:
            return True
        else:
            if query[self.axis] < self.data[self.axis]:
                return self.left.exists(query, tolerance)
            else:
                return self.right.exists(query, tolerance)


    def check_dimensionality(self, point):
        if len(point) != len(self.data):
            raise Exception('Dimensionality of data does not match KDTree dimension.')

    def get_distance(self, point):
        self.check_dimensionality(point)
        distance = 0

        for i in range(len(self.data)):
            distance += (self.data[i] - point[i]) ** 2

        return distance ** .5


if __name__ == '__main__':
    # Testing
    root = KDNode((1, 1))
    root = root.insert((4, 7))
    root = root.insert((-2, -2))
    root = root.insert((8, 2))
    root = root.insert((-6, 2))
    root = root.insert((5, 8))

    print(root.exists((-5, 3), 2))