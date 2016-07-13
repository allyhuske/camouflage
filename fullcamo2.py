from graphics import *
import random
import cProfile

#Screen settings
WIDTH = 1000
HEIGHT = 720

# Variables for adjusting evolution
start_dots = 20
mutation_range = 20
speed = .001
carrying_capacity = 30
simulation_length = 300
target_color1 = 120
target_color2 = 130
target_color3 = 140
max_fit = 10
max_fit_total = float((((max_fit ** 2) * 3) ** 0.5))
seed = 20

# Setup
win = GraphWin('practice', WIDTH, HEIGHT)
dot_dict = {}
backc = color_rgb(target_color1, target_color2, target_color3)
win.setBackground(backc)

# Creates n dots of random colors in random locations
def spawn_dots(n):
    dot_list = []
    for i in range(n):
        r_r = random.randrange(0,255)
        r_g = random.randrange(0,255)
        r_b = random.randrange(0,255)
        r_x = random.randrange(0,WIDTH)
        r_y = random.randrange(0,HEIGHT)
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


def predator(d):
#    print("PREDATOR WORKING")
    while len(d) > carrying_capacity:
        victim = random.choice(d)
        f = victim.fit
        chance_killed = (max_fit_total - f) / (max_fit_total)
        p = random.random()
        if chance_killed > p:
            victim.undraw_dot()
            d.remove(victim)
            del(victim)

# Creates dot class
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

    def reproduce(self):
        repro_p = (max_fit_total - float(self.fit)) / float(max_fit_total)
# Determines whether dot will reproduce
        if repro_p > random.random():
            self.color_flash('white')
# Determines number of offspring based on fitness
            if self.fit < ((max_fit_total) - 3):
                offspring = (int(self.fit) + 1)
            elif (max_fit_total - 3) <= self.fit < (max_fit_total - 2):
                offspring = (int(self.fit) + 1) * 2
            elif (max_fit_total - 2) <= self.fit < (max_fit_total - 1):
                offspring = (int(self.fit) + 1) * 4
            elif (max_fit_total - 1) <= self.fit:
                offspring = (int(self.fit) + 1) * 8

            dot_list = []
# Mutates one of the dot's colors
            for i in range(offspring):
                m_red = self.r
                m_green = self.g
                m_blue = self.b

                mut_value = random.randrange(2)
                if mut_value == 0:
                    m_red = mutate(self.r)
                elif mut_value == 1:
                    m_green = mutate(self.g)
                elif mut_value == 2:
                    m_blue = mutate(self.b)
                newd = Dot(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), m_red, m_green, m_blue)
                time.sleep(speed)
                newd.draw_dot()
                dot_list.append(newd)
                # print(newd.fit)
            self.color_flash('black')
            return dot_list
        else:
            return []
def simulation_step (parent_gen, fitlist):
    for i in range(len(parent_gen)):
        new_adults = parent_gen[i].reproduce()
        for j in new_adults:
            parent_gen.append(j)
    predator(parent_gen)

def loop(parent_gen, fitlist):
    for i in range(1000):
        simulation_step(parent_gen, fitlist)
    win.update()




# testing area
def evolve_record(start_dots, output):
    x = spawn_dots(start_dots)
    starting_fitness = str(fit_ave(x))
    output.write("Starting fitness: " + starting_fitness + '\n')
    parent_gen = x
    fitlist = []
    counter = 0
    while counter <=200:
        simulation_step(parent_gen, fitlist)
# Finds average fitness and writes to file
        popfit = fit_ave(parent_gen)
        output.write(str(popfit) + '\n')
        counter += 1

# runs program

def main():
    f = open("popfit.txt", "a")
    f.write("Experiment Settings:" + '\n')
    f.write("Number of starting dots: " + str(seed) + '\n')
    f.write("Mutation range: " + str(mutation_range) + '\n')
    f.write("Carrying capacity: " + str(carrying_capacity) + '\n')
    evolve_record(100, f)
    f.close()

if __name__=="__main__":
    cProfile.run("main()")
