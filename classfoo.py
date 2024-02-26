class A:
    def __init__(self):
        self.value = 'I am an A'
        self.value2 = 'really'
 
    def print(self):
        print(self.value)
        print(self.value2)
 
class B(A):
    def __init__(self):
        super().__init__()
        # self.value = 'I am a B'
 
a = A()
b = B()
a.print()
b.print()
