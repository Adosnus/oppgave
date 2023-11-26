class Arven():
    """
    Klasse som skal arves

    Parametre:
        x     (int): x kordinatene
        y     (int): y kordinatene
    """

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
    
    def pånytt_brikke(self):
        self.x = self.original_x
        self.y = self.original_y
    
    def pånytt_ball(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_fart = 0
        self.x_fart *= -1