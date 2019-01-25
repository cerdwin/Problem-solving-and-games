class Cuboid:
    def __init__(self, len_a, len_b, len_c):
        self.len_a = len_a
        self.len_b = len_b
        self.len_c = len_c
 
    def compute_volume(self):
        return self.len_a*self.len_b*self.len_c
 
    def make_scaled_copy(self, scale):
        return Cuboid(scale*self.len_a, scale*self.len_b, scale*self.len_c)
 
c1 = Cuboid(1, 2, 3)
print(c1.compute_volume())
 
c3 = c1.make_scaled_copy(2)
print(type(c3))
 
print(c3.compute_volume())
