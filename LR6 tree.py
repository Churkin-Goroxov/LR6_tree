class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:

    # высота узла
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # баланс узла
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # поворот вправо
    def right_rotate(self, y):
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        x.height = 1 + max(self.get_height(x.left),
                           self.get_height(x.right))

        return x

    # поворот влево
    def left_rotate(self, x):
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        x.height = 1 + max(self.get_height(x.left),
                           self.get_height(x.right))

        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        return y

    # добавление элемента
    def insert(self, root, key):

        # обычная вставка как в bst
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # обновляем высоту
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # проверяем баланс
        balance = self.get_balance(root)

        # левый левый случай
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # правый правый случай
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # левый правый случай
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # правый левый случай
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # минимальный элемент
    def get_min(self, node):
        current = node

        while current.left is not None:
            current = current.left

        return current

    # удаление элемента
    def delete(self, root, key):

        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)

        elif key > root.key:
            root.right = self.delete(root.right, key)

        else:

            # один ребенок или нет детей
            if root.left is None:
                return root.right

            elif root.right is None:
                return root.left

            # два ребенка
            temp = self.get_min(root.right)

            root.key = temp.key

            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        # обновляем высоту
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance(root)

        # левый левый
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # левый правый
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # правый правый
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # правый левый
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # вывод дерева
    def preorder(self, root):
        if not root:
            return

        print(root.key, end=" ")
        self.preorder(root.left)
        self.preorder(root.right)


# проверка AVL
print("AVL дерево")
tree = AVLTree()
root = None

nums = [10, 20, 30, 40, 50, 25]

for num in nums:
    root = tree.insert(root, num)

print("AVL после добавления:")
tree.preorder(root)

root = tree.delete(root, 40)

print("\nAVL после удаления:")
tree.preorder(root)

print("\n")


class RBNode:
    def __init__(self, key):
        self.key = key
        self.color = "red"
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.nil = RBNode(0)
        self.nil.color = "black"
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = None
        self.root = self.nil

    # левый поворот
    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    # правый поворот
    def right_rotate(self, y):
        x = y.left
        y.left = x.right

        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    # вставка
    def insert(self, key):
        node = RBNode(key)
        node.left = self.nil
        node.right = self.nil

        parent = None
        current = self.root

        while current != self.nil:
            parent = current

            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent

        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        # если корень
        if node.parent is None:
            node.color = "black"
            return

        # если дедушки нет
        if node.parent.parent is None:
            return

        self.fix_insert(node)

    # исправление дерева после вставки
    def fix_insert(self, k):
        while k.parent.color == "red":

            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left

                # дядя красный
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)

                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.left_rotate(k.parent.parent)

            else:
                u = k.parent.parent.right

                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)

                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.right_rotate(k.parent.parent)

            if k == self.root:
                break

        self.root.color = "black"

    # поиск минимального
    def minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    # замена узлов
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    # удаление
    def delete(self, key):
        z = self.root

        while z != self.nil:
            if z.key == key:
                break

            if key < z.key:
                z = z.left
            else:
                z = z.right

        if z == self.nil:
            return

        y = z
        y_original_color = y.color

        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)

        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)

        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "black":
            self.fix_delete(x)

    # исправление после удаления
    def fix_delete(self, x):
        while x != self.root and x.color == "black":

            if x == x.parent.left:
                s = x.parent.right

                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root

            else:
                s = x.parent.left

                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "black" and s.left.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "black"

    # вывод дерева
    def preorder(self, node):
        if node != self.nil:
            print(node.key, node.color)
            self.preorder(node.left)
            self.preorder(node.right)


# проверка красно-черного дерева
print("Красно-черное дерево")
tree = RBTree()

nums = [10, 20, 30, 15, 25, 5]

for num in nums:
    tree.insert(num)

print("RB дерево после добавления:")
tree.preorder(tree.root)

tree.delete(20)

print("\nRB дерево после удаления:")
tree.preorder(tree.root)