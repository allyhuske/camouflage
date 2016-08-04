################# DETERMINES INITIAL SETTINGS AND VARIABLES #################

from graphics import *
import random
import time

#Screen settings
WIDTH = 1000
HEIGHT = 720
win = GraphWin('camouflage', WIDTH + 200, HEIGHT)
panel_color = color_rgb(150, 150, 150)

# Automatic Variables
simulation_length = 200
max_fit = 10
max_fit_total = float((((max_fit ** 2) * 3) ** 0.5))
filename = "inputpopfit.txt"
fitper = ""
inprogress = False
fittext = Text(Point(2,2), "")


################# CREATES AND DRAWS USER CONTROL PANEL #################

panel = Rectangle(Point(WIDTH, 0), Point((WIDTH + 200), HEIGHT))
panel.setFill(panel_color)
panel.draw(win)

border = Line(Point(WIDTH,0), Point(WIDTH, HEIGHT))
border.draw(win)

# Creates button class
class Button(object):
    def __init__(self, corner_x, corner_y, width, length, text, cf):
        self.corner_x = corner_x
        self.corner_y = corner_y
        self.length = length
        self.width = width
        self.rect = Rectangle(Point(self.corner_x, self.corner_y), Point((self.corner_x + self.width), (self.corner_y + self.length)))
        self.text = text
        self.label = Text(Point((self.corner_x + (self.width / 2)), (self.corner_y + (self.length / 2))), self.text)
        self.cf = cf

    def draw_button(self, window):
        self.rect.draw(window)
        self.label.draw(window)

    def button_pushed(self, x, y):
        if self.corner_x < x and x < (self.corner_x + self.width) and self.corner_y < y and y < (self.corner_y + self.length):
            if self.cf:
                self.rect.setFill("white")
            return True
        else:
            return False

# Runs on automatic settings
auto_button = Button((WIDTH + 70), 20, 60, 35, "AUTO", True)
auto_button.draw_button(win)

# Gets mutation range
    # Creates and draws label
mri = Text(Point((WIDTH + 100), 80), "Mutation Range:")
mri.draw(win)

    # Creates and draws buttons
mr1_button = Button((WIDTH + 20), 95, 40, 35, "1", True)
mr2_button = Button((WIDTH + 80), 95, 40, 35, "2", True)
mr3_button = Button((WIDTH + 140), 95, 40, 35, "3", True)
mr1_button.draw_button(win)
mr2_button.draw_button(win)
mr3_button.draw_button(win)

# Gets carrying capacity
    # Creates and draws label
cci = Text(Point((WIDTH + 100), 155), "Carrying Capacity:")
cci.draw(win)

    # Creates and draws buttons
cc1_button = Button((WIDTH + 20), 170, 40, 35, "1", True)
cc2_button = Button((WIDTH + 80), 170, 40, 35, "2", True)
cc3_button = Button((WIDTH + 140), 170, 40, 35, "3", True)
cc1_button.draw_button(win)
cc2_button.draw_button(win)
cc3_button.draw_button(win)

# Gets initial population
    # Creates and draws label
ipi = Text(Point((WIDTH + 100), 230), "Initial Population:")
ipi.draw(win)

    # Creates and draws buttons
ip1_button = Button((WIDTH + 20), 245, 40, 35, "1", True)
ip2_button = Button((WIDTH + 80), 245, 40, 35, "2", True)
ip3_button = Button((WIDTH + 140), 245, 40, 35, "3", True)
ip1_button.draw_button(win)
ip2_button.draw_button(win)
ip3_button.draw_button(win)

# Gets speed
    # Creates and draws label
si = Text(Point((WIDTH + 100), 305), "Speed:")
si.draw(win)

    # Creates and draws buttons
speed1_button = Button((WIDTH + 20), 320, 40, 35, "1", True)
speed2_button = Button((WIDTH + 80), 320, 40, 35, "2", True)
speed3_button = Button((WIDTH + 140), 320, 40, 35, "3", True)
speed1_button.draw_button(win)
speed2_button.draw_button(win)
speed3_button.draw_button(win)

# Creates background changer button
bc_button = Button((WIDTH + 30), 500, 140, 70, "Change Background", False)
bc_button.draw_button(win)

# Creates stop button
pause_button = Button((WIDTH + 30), 610, 140, 70, "Pause", False)
pause_button.draw_button(win)

# Creates popfit text
fitperl = Text(Point((WIDTH + 100), 405), "Population fitness:")

# Creates stopped screen text
stoptext = Text(Point((WIDTH + 100), 475), "Click anywhere to continue")



################# CREATES FUNCTIONS NECESSARY FOR EVOLUTION #################

# Creates n dots of random colors in random locations
def spawn_dots(n):
    dot_list = []
    for i in range(n):
        r_r = random.randrange(0,255)
        r_g = random.randrange(0,255)
        r_b = random.randrange(0,255)
        r_x = random.randrange(10,WIDTH - 10)
        r_y = random.randrange(10,HEIGHT - 10)
        dot1 = Dot(r_x, r_y, r_r, r_g, r_b)
        dot1.draw_dot()
        dot_list.append(dot1)
    return dot_list

# Causes a random mutation in color
def mutate(x):
    if x + mutation_range <= 255 and x - mutation_range >= 0:
        new_x = abs(random.randrange((x - mutation_range), (x + mutation_range)))
        return new_x
    elif x + mutation_range <= 255 and x - mutation_range < 0:
        new_x = abs(random.randrange(0, (x + mutation_range)))
        return new_x
    elif x + mutation_range > 255 and x - mutation_range >= 0:
        new_x = abs(random.randrange((x - mutation_range), 255))
        return new_x
    elif x + mutation_range > 255 and x - mutation_range < 0:
        new_x = abs(random.randrange(0, 255))
        return new_x

def fit_ave(values):
    total = 0
    for i in values:
        total += i.fit
    ave = float(total) / len(values)
    return (ave / max_fit_total)

# Determines fitness level based on all colors
def fitness_function(red, green, blue):
# Determines red fitness
    rd = float(abs(target_color1 - red))
    if target_color1 >= (255 - target_color1):
        max_c = target_color1
    if (255 - target_color1) > target_color1:
        max_c = 255 - target_color1
    rfit = ((max_c - rd)/max_c) * max_fit
# Determines green fitness
    gd = float(abs(target_color2 - green))
    if target_color2 >= (255 - target_color2):
        max_c = target_color2
    if (255 - target_color2) > target_color2:
        max_c = 255 - target_color2
    gfit = ((max_c - gd)/max_c) * max_fit
# Determines blue fitness
    bd = float(abs(target_color3 - blue))
    if target_color3 >= (255 - target_color3):
        max_c = target_color3
    if (255 - target_color3) > target_color3:
        max_c = 255 - target_color3
    bfit = ((max_c - bd)/max_c) * max_fit
# Determines and returns combined fitness
    fit = (rfit**2 + gfit**2 + bfit**2)**0.5
    return fit

def undraw_all_dots(d):
    for i in d:
        i.undraw_dot()
    win.update()

def predator(d):
    a_d = list(d)
    while len(a_d) > carrying_capacity:
        victim = random.choice(a_d)
        f = victim.fit
        chance_killed = ((max_fit_total - f + .001) * 2) / (max_fit_total)
        p = random.random()
        if chance_killed > p:
            a_d.remove(victim)
            win.update()
    return a_d


################# CREATES DOT CLASS #################

class Dot(object):
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.color = color_rgb(self.r, self.g, self.b)
        self.fit = fitness_function(self.r, self.g, self.b)
        self.circle = Circle(Point(self.x, self.y), 10)

    def draw_dot(self):
        self.circle.setFill(self.color)
        self.circle.draw(win)

    def undraw_dot(self):
        self.circle.undraw()

    def color_flash(self, color):
        self.circle.setOutline(color)
        win.update()

    def reproduce(self, win):
        repro_p = ((float(self.fit)) / float(max_fit_total) * .25)
        k = random.random()
# Determines whether dot will reproduce
        if repro_p > k:
            self.color_flash('white')
# Determines number of offspring based on fitness
            offspring = (int(self.fit) + 1)
            dot_list = []
# Mutates one of the dot's colors
            for i in range(offspring):
                mut_value = random.randrange(3)
                if mut_value == 0:
                    m_red = mutate(self.r)
                    m_green = self.g
                    m_blue = self.b
                elif mut_value == 1:
                    m_red = self.r
                    m_green = mutate(self.g)
                    m_blue = self.b
                elif mut_value == 2:
                    m_red = self.r
                    m_green = self.g
                    m_blue = mutate(self.b)
                newd = Dot(random.randrange(10, WIDTH - 10), random.randrange(10, HEIGHT - 10), m_red, m_green, m_blue)
                time.sleep(speed)
                newd.draw_dot()
                dot_list.append(newd)
                win.update()
            self.color_flash('black')
            return dot_list
        else:
            return []


################# DEFINES EVOLUTION FUNCTION #################

def evolve_record(start_dots):
# writes variables and conditions to file
    file = open(filename, "a")
    file.write("Experiment Settings:" + '\n')
    file.write("Number of starting dots: " + str(seed) + '\n')
    file.write("Mutation range: " + str(mutation_range) + '\n')
    file.write("Carrying capacity: " + str(carrying_capacity) + '\n')
    file.write("Speed: " + str(speed) + '\n')
    file.close()
# sets beginning population
    if type(start_dots) == int:
        population = spawn_dots(start_dots)
    else:
        population = start_dots
# calculates fitness of initial population and write to file
    starting_fitness = str(fit_ave(population))
    file = open(filename, "a")
    file.write("Starting fitness: " + starting_fitness + '\n')
    file.close()
# begins evolution
    counter = 0
    t0 = time.time()
    while (time.time() - t0) <= 360:
        stopped = False
        global target_color1
        global target_color2
        global target_color3
        global inprogress
        global fittext
        new_adults = []

        for i in population:
            # Checks for background change or pause
            q = win.checkMouse()
            if not q == None:
                x = q.getX()
                y = q.getY()
                if bc_button.button_pushed(x, y):
                    target_color1 = random.randrange(0, 255)
                    target_color2 = random.randrange(0, 255)
                    target_color3 = random.randrange(0, 255)
                    win.setBackground(color_rgb(target_color1, target_color2, target_color3))
                    win.update()
                    file = open(filename, "a")
                    file.write("Background color changed")
                    file.close()
                if pause_button.button_pushed(x, y):
                    stoptext.draw(win)
                    win.update()
                    v = win.getMouse()
            stoptext.undraw()
            win.update()
            # Causes all dots in population to reproduce and add to new_adults
            new_adults = new_adults + i.reproduce(win)
        # Adds new generation to population, calls predator on population
        population = population + new_adults
        updatedpop = predator(population)
        undraw_all_dots(population)
        # Draws new population
        for i in updatedpop:
            # Checks for background change or pause
            q = win.checkMouse()
            if not q == None:
                x = q.getX()
                y = q.getY()
                if bc_button.button_pushed(x, y):
                    target_color1 = random.randrange(0, 255)
                    target_color2 = random.randrange(0, 255)
                    target_color3 = random.randrange(0, 255)
                    win.setBackground(color_rgb(target_color1, target_color2, target_color3))
                    win.update()
                    file = open(filename, "a")
                    file.write("Background color changed" + '\n')
                    file.close()
                if pause_button.button_pushed(x, y):
                    stoptext.draw(win)
                    win.update()
                    v = win.getMouse()
            stoptext.undraw()
            win.update()
            i.draw_dot()
        win.update()
        population = updatedpop
# Finds average fitness and writes to file
        popfit = fit_ave(population)
        timecount = time.time() - t0
        file = open(filename, "a")
        file.write(str(timecount) + " " + str(popfit) + '\n')
        file.close()
# Writes fitness to control panel
        if inprogress:
            fittext.undraw()
        fitper = str(popfit * 100) + "%"
        fittext = Text(Point(WIDTH + 100, 425), fitper)
        fittext.setSize(20)
        fitperl.undraw()
        fitperl.draw(win)
        fittext.draw(win)
        win.update()
        counter += 1
        inprogress = True
    return population



################# DEFINES MAIN FUNCTION #################
def main():
    # Sets initial variables
    global seed
    global mutation_range
    global carrying_capacity
    global speed
    global target_color1
    global target_color2
    global target_color3

    target_color1 = 150
    target_color2 = 150
    target_color3 = 150
    backc = color_rgb(target_color1, target_color2, target_color3)
    win.setBackground(backc)

    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    # Gets user input and sets more variables
    while counter1 == 0 or counter2 == 0 or counter3 == 0 or counter4 == 0:
        p = win.getMouse()
        x = p.getX()
        y = p.getY()
        # Sets mutation_range
        if counter1 != 1:
            if mr1_button.button_pushed(x, y):
                mutation_range = 5
                counter1 = 1
            if mr2_button.button_pushed(x, y):
                mutation_range = 20
                counter1 = 1
            if mr3_button.button_pushed(x, y):
                mutation_range = 50
                counter1 = 1

        # Sets carrying capacity
        if counter2 != 1:
            if cc1_button.button_pushed(x, y):
                carrying_capacity = 10
                counter2 = 1

            if cc2_button.button_pushed(x, y):
                carrying_capacity = 30
                counter2 = 1

            if cc3_button.button_pushed(x, y):
                carrying_capacity = 50
                counter2 = 1

        # Sets initial population size
        if counter3 != 1:
            if ip1_button.button_pushed(x, y):
                seed = 10
                counter3 = 1
            if ip2_button.button_pushed(x, y):
                seed = 20
                counter3 = 1
            if ip3_button.button_pushed(x, y):
                seed = 30
                counter3 = 1

        # Sets speed
        if counter4 != 1:
            if speed1_button.button_pushed(x, y):
                speed = .1
                counter4 = 1
            if speed2_button.button_pushed(x, y):
                speed = .01
                counter4 = 1
            if speed3_button.button_pushed(x, y):
                speed = 0
                counter4 = 1

        # Sets all variables to auto
        if counter1 != 1 and counter2 != 1 and counter3 != 1 and counter4 != 1:
            if auto_button.button_pushed(x, y):
                mutation_range = 20
                carrying_capacity = 30
                seed = 15
                speed = 0
                counter1 = 1
                counter2 = 1
                counter3 = 1
                counter4 = 1

    # Calls evolve function
    a = evolve_record(seed)

################# RUNS FULL PROGRAM #################

main()
win.mainloop()
