class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.comparisons = 0

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        self.comparisons = 0
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        self.comparisons += 1
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.right = self._delete(node.right, min_node.key)
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def level_order(self):
        if self.root is None:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result


keys_sorted = [1, 2, 3, 4, 5, 6, 7]
bst_sorted = BST()
for k in keys_sorted:
    bst_sorted.insert(k)
keys_balanced = [4, 2, 6, 1, 3, 5, 7]
bst_balanced = BST()
for k in keys_balanced:
    bst_balanced.insert(k)

print("Высоты:")
print(f"Сортированный {bst_sorted.height()}")
print(f"Сбалансированный {bst_balanced.height()}")



test_elements = [7]
print("\nСравнение количества сравнений при поиске:")
print("Искать:\tСравнения (сорт)\tСравнения (баланс)\tнайдено (сорт)\tнайдено(баланс)")
for elem in test_elements:
    res_sorted = bst_sorted.search(elem)
    cmp1 = bst_sorted.comparisons
    res_balanced = bst_balanced.search(elem)
    cmp2 = bst_balanced.comparisons
    print(f"{elem}\t{cmp1}\t\t\t{cmp2}\t\t\t{res_sorted}\t\t\t{res_balanced}")