import math
import random as rand
from pyswarm import pso


def objective_function(particle):
    x = particle[0]
    y = particle[1]
    return -abs(math.sin(x)*math.cos(y)*math.exp(abs(1-((math.sqrt(x**2+y**2))/math.pi))))


def swarm_maker(lowerBond, UpperBond, swarmSize): #It would generate a swarm is size of swarmSize with specific bound
    swarm = []
    for i in range(swarmSize):
        particle = []
        x = rand.uniform(lowerBond,UpperBond)
        y = rand.uniform(lowerBond,UpperBond)
        v_x = 0
        v_y = 0
        best_x = x
        best_y = y
        particle.append(x)
        particle.append(y)
        particle.append(v_x)
        particle.append(v_y)
        particle.append(best_x)
        particle.append(best_y)
        swarm.append(particle)
    return swarm


def calcBestGlobal(swarm):
    best = objective_function(swarm[0])
    index = 0
    for i in range(len(swarm)):
        temp = objective_function(swarm[i])
        if temp < best:
            best = temp
            index = i
    return swarm[index]


def update_velocity(particle, g_best, w, c1, c2):
    i = 0
    while i < 2:
        r1 = rand.random()
        r2 = rand.random()
        inertia_i = w * particle[i+2]
        cognitive_i = c1 * r1 * (particle[i+4] - particle[i])
        social_i = c2 * r2 * (g_best[i] - particle[i])
        particle[i+2] = inertia_i + cognitive_i + social_i
        i += 1


def update_position(particle):
    particle[0] = particle[0] + particle[2]
    if particle[0] > 10 or particle[0] < -10:
        particle[0] = particle[0] - particle[2]
    particle[1] = particle[1] + particle[3]
    if particle[1] > 10 or particle[1] < -10:
        particle[1] = particle[1] - particle[3]


def PSO(lowerBond, upperBond, swarmSize, c1, c2, w, iteration):
    swarm = swarm_maker(lowerBond, upperBond, swarmSize)
    for i in range(iteration):
        g_best = calcBestGlobal(swarm)
        for j in range(swarmSize):
            update_velocity(particle=swarm[j], g_best=g_best, w=w, c1=c1, c2=c2)
            update_position(swarm[j])
    solution = calcBestGlobal(swarm)
    result = [solution[0], solution[1]]

    return objective_function(result), result


lbound = [-10, -10]
ubound = [10, 10]
print("Number at the end is the average precision of my implementation to Python's Default implementation after 100times :")
m = n = 0
for i in range(100):
    bestResult, bestParticle =PSO(-100, 100, 200, 0.5, 0.5, 0.5, 200)
    default_bestP, default_bestR = pso(func=objective_function,lb=lbound,ub=ubound)
    m += bestResult
    n += default_bestR
print(m/n*100)