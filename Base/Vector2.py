class Vector2:
    def __init__(self, x, y):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise TypeError("Vector2 类型的构造参数只支持 int 或 float 类型")
        self.x = float(x)
        self.y = float(y)
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2(self.x / scalar, self.y / scalar)
        raise TypeError("除法运算只支持标量类型 (int 或 float)")
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2(self.x * scalar, self.y * scalar)
        raise TypeError("乘法运算只支持标量类型 (int 或 float)")
    def __rmul__(self, other):
        return self.__mul__(other)
    def __str__(self):
        return f"({self.x}, {self.y})"