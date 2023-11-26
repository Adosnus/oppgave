import pygame
import sys
from pongarv import Arven

pygame.init()

BREDDE = 700
HOYDE = 500
FPS = 60
vindu = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("Pong")
klokke = pygame.time.Clock()

HVIT = (255, 255, 255)
SVART = (0, 0, 0)

Brikke_hoyde = 100
Brikke_bredde = 20

Ball_radius = 7


peong = pygame.font.SysFont("comicsand", 50)



class Brikke(Arven):
    """
    Klasse som skal arves

    Parametre:
        x        (int): x kordinatene
        y        (int): y kordinatene
        bredde   (int): bredden på brikken
        hoyde    (int): høyden på brikken
    """
    fart = 7
    def __init__(self, x: int, y: int, bredde: int, hoyde: int):
        super().__init__(x, y)
        self.bredde = bredde
        self.hoyde = hoyde

    def tegn(self, vindu):
        pygame.draw.rect(vindu, HVIT, (self.x, self.y, self.bredde, self.hoyde))
    
    def beveg(self, up=True):
        if up:
            self.y -= self.fart
        else:
            self.y += self.fart 

class Ball(Arven):
    """
    Klasse som skal arves

    Parametre:
        x        (int): x kordinatene
        y        (int): y kordinatene
        radius   (int): radius på ballen
    """
    ball_fart = 6 * 1.5
    def __init__(self, x: int, y: int, radius: int):
        super().__init__(x, y)
        self.radius = radius
        self.x_fart = self.ball_fart
        self.y_fart = 0

    def tegn(self, vindu):
        pygame.draw.circle(vindu, HVIT, (self.x, self.y), self.radius)

    def beveg(self):
        self.x += self.x_fart
        self.y += self.y_fart

def tegn(vindu, brikker, ball, venstre_poeng, hoyre_poeng):
    vindu.fill(SVART)

    venstre_peong_text = peong.render(f"{venstre_poeng}", 1, HVIT)
    hoyre_peong_text = peong.render(f"{hoyre_poeng}", 1, HVIT)
    vindu.blit(venstre_peong_text, (BREDDE // 4 - venstre_peong_text.get_width()//2, 20))
    vindu.blit(hoyre_peong_text, (BREDDE * (3/4)- hoyre_peong_text.get_width()//2, 20))

    for brikke in brikker:
        brikke.tegn(vindu)

    ball.tegn(vindu)

def kollisjoner(ball, venstre_brikke, hoyre_brikke):
    if ball.y + ball.radius >= HOYDE:
        ball.y_fart *= -1
    elif ball.y - ball.radius <=0:
        ball.y_fart *= -1
    
    if ball.x_fart < 0:
        if ball.y >= venstre_brikke.y and ball.y <= venstre_brikke.y + venstre_brikke.hoyde:
            if ball.x - ball.radius <= venstre_brikke.x + venstre_brikke.bredde:
                ball.x_fart *= -1

                senter_y = venstre_brikke.y + venstre_brikke.hoyde / 2
                y_forskjell = senter_y - ball.y
                faktoren = (venstre_brikke.hoyde / 2) / ball.ball_fart
                y_fart = y_forskjell / faktoren
                ball.y_fart = -y_fart
    else:
        if ball.y >= hoyre_brikke.y and ball.y <= hoyre_brikke.y + hoyre_brikke.hoyde:
            if ball.x + ball.radius >= hoyre_brikke.x:
                ball.x_fart *= -1
                
                senter_y = hoyre_brikke.y + hoyre_brikke.hoyde / 2
                y_forskjell = senter_y - ball.y
                faktoren = (venstre_brikke.hoyde / 2) / ball.ball_fart
                y_fart = y_forskjell / faktoren
                ball.y_fart = -y_fart

def brikke_bevegelse(taster, venstre_brikke, hoyre_brikke):
    if taster[pygame.K_w] and venstre_brikke.y - venstre_brikke.fart >= 0:
        venstre_brikke.beveg(up=True)
    if taster[pygame.K_s] and venstre_brikke.y + venstre_brikke.fart + venstre_brikke.hoyde <= HOYDE:
        venstre_brikke.beveg(up=False)
    
    if taster[pygame.K_UP] and hoyre_brikke.y - hoyre_brikke.fart >= 0:
        hoyre_brikke.beveg(up=True)
    if taster[pygame.K_DOWN] and hoyre_brikke.y + hoyre_brikke.fart + hoyre_brikke.hoyde <= HOYDE:
        hoyre_brikke.beveg(up=False)

ball = Ball(HOYDE // 2, HOYDE // 2, Ball_radius)

def main():
    venstre_brikke = Brikke(10, HOYDE//2 - Brikke_hoyde//2, Brikke_bredde, Brikke_hoyde)
    hoyre_brikke = Brikke(BREDDE - 10 - Brikke_bredde, HOYDE//2 - Brikke_hoyde//2, Brikke_bredde, Brikke_hoyde)

    venstre_poeng = 0
    hoyre_poeng = 0
    while True:
        for hendelse in pygame.event.get():
            if hendelse.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        taster = pygame.key.get_pressed()

        ball.beveg()

        kollisjoner(ball, venstre_brikke, hoyre_brikke)
        brikke_bevegelse(taster, venstre_brikke, hoyre_brikke)
        pygame.draw.rect(vindu, HVIT, pygame.Rect(BREDDE // 2 - 5, 0, 10, HOYDE))  
        pygame.display.flip()
        klokke.tick(FPS)

        if ball.x <= 0:
            hoyre_poeng += 1
            ball.pånytt_ball()
            venstre_brikke.pånytt_brikke()
            hoyre_brikke.pånytt_brikke()
            
        elif ball.x >= BREDDE:
            venstre_poeng +=1
            ball.pånytt_ball()
            venstre_brikke.pånytt_brikke()
            hoyre_brikke.pånytt_brikke()

        if hoyre_poeng == 20:
            vindu.fill(SVART)
            winner_text = peong.render(("Høyre vant"), True, HVIT)
            vindu.blit(winner_text, (BREDDE // 2 - 100, HOYDE // 2 - 18))
            pygame.display.flip()
            pygame.time.delay(3000)  
            break 

        elif venstre_poeng == 20:
            vindu.fill(SVART)
            winner_text2 = peong.render(("Venstre vant"), True, HVIT)
            vindu.blit(winner_text2, (BREDDE // 2 - 100, HOYDE // 2 - 18))
            pygame.display.flip()
            pygame.time.delay(3000)  
            break  

        tegn(vindu, [venstre_brikke, hoyre_brikke], ball, venstre_poeng, hoyre_poeng)


if __name__ == "__main__":
    main()