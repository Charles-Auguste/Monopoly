import pygame_textinput
import pygame
import pygame.locals as pl
from color import *
import time
pygame.init()

screen_width, screen_height = 1500,1500
main_screen = pygame.display.set_mode((screen_width,screen_height))

def text_format(message, textSize, textColor):
    newFont = pygame.font.SysFont("Consolas", textSize)
    newText = newFont.render(message, True, textColor)
    return newText

def print_text(screen,nb_ligne, text, textSize, textColor):
    txt = text_format(text, textSize, textColor)
    y_init = nb_ligne*height//(nb_lignes+1)
    x_init = (width-height) + 100
    screen.blit(txt, (x_init, y_init))


class Text_input_box:
    def __init__(self,width = 200, height = 40, x_init = 10, y_init = 10, screen = None, visible_after : bool = True, validate = lambda input: len(input) <= 17):
        self.manager = pygame_textinput.TextInputManager(validator=validate)
        self.font = pygame.font.SysFont("Consolas", 20)
        self.textinput = pygame_textinput.TextInputVisualizer(manager=self.manager, font_object=self.font)
        self.width = width
        self.height = height
        self.x_init = x_init
        self.y_init = y_init
        self.clock = pygame.time.Clock()
        self.visible = visible_after
        if screen == None:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        else:
            self.screen = screen

    def show_box (self):
        text_written = ""
        go = True
        while go:
            pygame.draw.rect(self.screen, white, pygame.Rect(self.x_init, self.y_init, self.width, self.height))
            events = pygame.event.get()
            # Feed it with events every frame
            self.textinput.update(events)
            # Blit its surface onto the screen
            self.screen.blit(self.textinput.surface, (self.x_init + 10 ,self.y_init))
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        text_written = self.textinput.value
                        go = False
            pygame.display.update()
            self.clock.tick(40)
        pygame.draw.rect(self.screen, white, pygame.Rect(self.x_init, self.y_init, self.width, self.height))
        pygame.display.update()
        if self.visible:
            text_end = text_format(text_written, 20, black)
            self.screen.blit(text_end,
                              (self.x_init + 10 , self.y_init))
            pygame.display.update()
        return text_written

class Terminal():
    """Create a 'terminal' in a pygame surface with 10-15 lines"""

    def __init__(self,x, y, scr, width_t = 500, height_t = 1000):
        """initialise the terminal in coordinates (x_init,y_init)"""
        self.screen = scr
        self.x_init = x
        self.y_init = y
        self.width = width_t
        self.height = height_t
        pygame.draw.rect(self.screen, white, pygame.Rect(self.x_init, self.y_init - 10, self.width, self.height + 10))
        pygame.display.update()

    def clear_all(self):
        """clean the terminal"""
        pygame.draw.rect(self.screen, white, pygame.Rect(self.x_init, self.y_init, self.width, self.height))
        pygame.display.update()

    def print_line(self,text, nb_line, color=black, size=20):
        """print 'text' on the line nb_line"""
        y_coordinate = (self.height//40) * nb_line
        text_to_print = text_format(text, size, color)
        self.screen.blit(text_to_print, (self.x_init + 10, self.y_init + y_coordinate))
        pygame.display.update()
        return(nb_line + 1)

    def clear_line(self, nb_line):
        """clear the text on line nb_line"""
        y_coordinate = (self.height // 40) * nb_line
        pygame.draw.rect(self.screen, white, pygame.Rect(self.x_init, self.y_init + y_coordinate, self.width, 20))
        pygame.display.update()

    def print_input(self, nb_line, visible_aft = True, validate = lambda input: len(input) <= 17 ):
        y_coordinate = (self.height // 40) * nb_line
        box = Text_input_box(screen=self.screen,x_init= self.x_init+10, y_init=self.y_init + y_coordinate, visible_after=visible_aft, validate = validate)
        text_receive = box.show_box()
        pygame.display.update()
        return [text_receive,nb_line+1]


if __name__ == "__main__":

    term = Terminal(screen_width//2 - 250 ,50,main_screen)
    for i in range(39):
        if (i%2 == 1):
            T = term.print_input(i)
            if T[0:5] == "clear":
                term.clear_all()
        else:
            term.print_line("---Name "+str(i//2 + 1),i, color=bleu_fonce)
    term.clear_all()
    for i in range(39):
        if (i == 0):
            term.print_line("-test : une ligne sur 3 effacée-", i, color=red)
        else:
            term.print_line("test ligne " + str(i), i, color=marron)
        if (i%3 == 0):
            term.clear_line(i-1)
        time.sleep(0.5)
    time.sleep(3)



    go = True
    term.clear_all()
    term.print_line("Presentation terminée",0, color=red)
    term.print_line("Appuyez sur ECHAP pour quitter", 1, color=red)
    while go:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                go = False
            if event.type == pygame.QUIT:
                go = False

    pygame.quit()

