################# DETERMINES INITIAL SETTINGS AND VARIABLES #################

from graphics import *
import random

#Screen settings
WIDTH = 1000
HEIGHT = 720

# Variables for adjusting evolution
mutation_range = 20
carrying_capacity = 30
simulation_length = 2000
target_color1 = 120
target_color2 = 130
target_color3 = 140
max_fit = 10
max_fit_total = float((((max_fit ** 2) * 3) ** 0.5))
seed = 20
filename = "fastpopfit.txt"

# Setup
win = GraphWin('camouflage', WIDTH, HEIGHT)
backc = color_rgb(target_color1, target_color2, target_color3)
win.setBackground(backc)


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
                dot_list.append(newd)
            return dot_list
        else:
            return []


################# DEFINES EVOLUTION FUNCTION #################

def evolve_record(start_dots):
# writes experiment conditions to file
    file = open(filename, "a")
    file.write("Experiment Settings:" + '\n')
    file.write("Number of starting dots: " + str(seed) + '\n')
    file.write("Mutation range: " + str(mutation_range) + '\n')
    file.write("Carrying capacity: " + str(carrying_capacity) + '\n')
    file.close()
# sets initial population
    if type(start_dots) == int:
        population = spawn_dots(start_dots)
    else:
        population = start_dots
    initpop = list(population)
# calculates initial fitness and writes to file
    starting_fitness = str(fit_ave(population))
    file = open(filename, "a")
    file.write("Starting fitness: " + starting_fitness + '\n')
    file.close()
# begins evolution
    counter = 0
    while counter <=simulation_length:
        new_adults = []
        for i in population:
            new_adults = new_adults + i.reproduce(win)
        population = predator(population + new_adults)
# Finds average fitness and writes to file
        popfit = fit_ave(population)
        file = open(filename, "a")
        file.write(str(popfit) + '\n')
        file.close()
        counter += 1
    undraw_all_dots(initpop)
    for i in population:
        i.draw_dot()
    return population

################# RUNS FULL PROGRAM #################

evolve_record(seed)
win.mainloop()
