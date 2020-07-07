import os
import time
import random
import math
from tkinter import *
import numpy as np


random.seed(time.time())

class Rocket:


    def __init__(self, c, dna,canvas,root,endPoint):
        self.startX = 250
        self.startY = 490
    
        self.height = 20
        self.width = 5
    
        self.upForce = -5
        self.stuck = False
        self.hit_target = False;

        self.dna = dna

        self.sideForce = 270
        self.fitness = 0

        self.x0 = self.startX
        self.y0 = self.startY
        self.x1 = self.startX
        self.y1 = self.y0 + self.height
        
        self.r = root
        self.c=canvas

        self.visual = self.c.create_line(self.x0, self.y0, self.x1, self.y1, width = self.width, fill="white")
        
        self.minDist = 100000000
        self.endPoint = endPoint
    def draw(self, c, current,color='white'):
        self.sideForce += self.dna[current]
        self.radAngle = (self.sideForce * math.pi) / 180

        self.x0 = self.x0 + self.upForce * -math.cos(self.radAngle)
        self.y0 = self.y0 + self.upForce * -math.sin(self.radAngle)
        self.x1 = self.x0 + self.height * math.cos(self.radAngle)
        self.y1 = self.y0 + self.height * math.sin(self.radAngle)

        self.visual = self.c.create_line(self.x0, self.y0, self.x1, self.y1, width = self.width, fill = color)

        #test collision
        #side of screen
        if self.x1 > 500 or self.x1 < 0:
            self.stuck = True
        if self.y1 > 500 or self.y1 < 0:
            self.stuck = True
        #obstacles
        if self.x1 > 150 and self.x1 < 350 and self.y1 > 240 and self.y1 < 250:
            self.stuck = True
        if self.x1 > 50 and self.x1 < 150 and self.y1 > 140 and self.y1 < 150:
            self.stuck = True
        if self.x1 > 350 and self.x1 < 450 and self.y1 > 140 and self.y1 < 150:
            self.stuck = True
        if self.x1 > 50 and self.x1 < 150 and self.y1 > 350 and self.y1 < 360:
            self.stuck = True
        if self.x1 > 350 and self.x1 < 450 and self.y1 > 350 and self.y1 < 360:
            self.stuck = True
        #goal
        if self.x1 > endPoint[0] - 10 and self.x1 < endPoint[0] + 10 and self.y1 > endPoint[1] - 10 and self.y1 < endPoint[1] + 10:
            self.stuck = True
            self.hit_target = True
            
        self.minDist = np.min([self.minDist,(math.sqrt((endPoint[0] - self.x1) ** 2 + (endPoint[1] - self.y1) ** 2))])
        self.c.pack()
        self.r.update_idletasks()
        self.r.update()

    def calcFit(self):
        # self.fitness = math.sqrt((self.startX - self.x1) ** 2 + (self.startY - self.y1) ** 2)
        # self.fitness = self.fitness - (math.sqrt((endPoint[0] - self.x1) ** 2 + (endPoint[1] - self.y1) ** 2))
        self.fitness = self.minDist+(math.sqrt((endPoint[0] - self.x1) ** 2 + (endPoint[1] - self.y1) ** 2))
        self.fitness = math.floor(self.fitness)

        # if (self.fitness <= 0):
        #     self.fitness = 1

        if (self.hit_target):
            self.fitness = -750

        return self.fitness

    def reset(self, c, dna):
        self.stuck = False
        self.hit_target = False

        self.dna = dna

        self.sideForce = 270
        self.fitness = 0

        self.c.delete(self.visual)

        self.x0 = self.startX
        self.y0 = self.startY
        self.x1 = self.startX
        self.y1 = self.y0 + self.height

rockets = []
genePool = []

popSize = 20
lifespan = 550
generationCounter = 1

# endPoint = (250, 50)
endPoint = (int(random.uniform(50,450)), int(random.uniform(50,450)))

root = Tk()
root.title('smart rockets')
root.resizable(False, False)
    
canvas = Canvas(root, height = 500, width = 500, bg = 'black')
generationText = canvas.create_text(10, 10, anchor = 'nw', fill = 'white', font = 20)

canvas.itemconfig(generationText, text = "generation 1")


visualObstacle = canvas.create_rectangle(150, 250, 350, 240, fill = "white")
visualObstacle2 = canvas.create_rectangle(50, 150, 150, 140, fill = "white")
visualObstacle3 = canvas.create_rectangle(350, 150, 450, 140, fill = "white")
visualObstacle4 = canvas.create_rectangle(50, 360, 150, 350, fill = "white")
visualObstacle5 = canvas.create_rectangle(350, 360, 450, 350, fill = "white")

for i in range(popSize):
    newDNA = []

    for j in range(lifespan):
        newDNA.append(random.uniform(-10, 10))

    newRocket = Rocket(canvas, newDNA,canvas,root,endPoint)
    rockets.append(newRocket)

visualEND = canvas.create_rectangle(endPoint[0] - 10, endPoint[1] - 10, endPoint[0] + 10, endPoint[1] + 10, fill = "green")

while 1:
    #run through simulation
    for i in range(lifespan):
        all_stuck = True

        for rocket in rockets:
            if rocket.stuck == False:
                canvas.delete(rocket.visual)
                rocket.draw(canvas, i)

                # canvas.pack()
                # root.update_idletasks()
                # root.update()

                all_stuck = False

        if (all_stuck == False):
            time.sleep(0.01)

    # time.sleep(1)

    #calc fitness
    fitness = []
    for rocket in rockets:
        fitness.append(rocket.calcFit())

              
    parent1 = rockets[np.argsort(fitness)[0]]#random.choice(genePool)
    parent2 = rockets[np.argsort(fitness)[1]]#random.choice(genePool)
    parent1.draw(canvas,i,'red')
    parent2.draw(canvas,i,'red')

    time.sleep(1)
    for rocket in rockets:
        canvas.delete(rocket.visual)
    #create new population
    for i in range(popSize):
        newDNA = []

        #use 2 most fit rockets


        #randomly pick a dna from a parent
        for j in range(lifespan):
            parents = [parent1.dna[j], parent2.dna[j]]
            _ = random.choice(parents)
            newDNA.append(_)

        #mutate
        if random.randint(0, 2) == 0:
            for j in range(math.floor(lifespan / 20)):
                randIndex = random.randint(0, lifespan - 1)
                _=newDNA.pop(randIndex)
                newDNA.insert(randIndex, random.uniform(-30, 30))
        #mutate, rare but big
        if random.randint(0, 20) == 0:
            for j in range(math.floor(lifespan / 20)):
                randIndex = random.randint(0, lifespan - 1)
                _=newDNA.pop(randIndex)
                newDNA.insert(randIndex, random.uniform(-100, 100))
        
        if i==0:
            rockets[i].reset(canvas, parent1.dna)
        elif i==1:
            rockets[i].reset(canvas, parent2.dna)
        else:
            rockets[i].reset(canvas, newDNA)

    genePool.clear()
    generationCounter = generationCounter + 1
    canvas.itemconfig(generationText, text = ("generation " + str(generationCounter)))
