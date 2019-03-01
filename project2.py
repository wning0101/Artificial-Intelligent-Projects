import random
import sys

if len(sys.argv) != 3 :
    print "Argument Error"
    print "Usage: python HW2.py Number_Of_Population Number_Of_Max_Iteration"
    exit()
population = int(sys.argv[1])
max_iteration = int(sys.argv[2])
fitness_max = 9


def initial_status():
    # type: () -> list
    status = []
    for i in range(8):
        temp = random.randint(0, 7)
        status.append(temp)
    return status

def swap(first, second):
    section = random.randint(1, 7)
    temp1 = []
    temp2 = []
    for j in first:
        temp1.append(j)
    for k in second:
        temp2.append(k)
    for i in range(section):
        temp1[i] = second[i]
        temp2[i] = first[i]
    return [temp1, temp2]

def produce(current, chart):
    temp = []
    for i in range(len(current)/2):
        first_select = 0
        second_select = 0
        while(first_select == second_select):
            first_random = random.randint(1, 100)
            segment = 0
            for i in range(len(chart)):
                segment += chart[i][0]
                if segment >= first_random:
                    first_select = i
                    break
            segment = 0
            second_random = random.randint(1, 100)
            for i in range(len(chart)):
                segment += chart[i][0]
                if segment >= second_random:
                    second_select = i
                    break
        #print first_select, second_select
        children = swap(current[first_select], current[second_select])
        temp.append(children[0])
        temp.append(children[1])
        #print temp
    return temp

def mutate(current):
    for i in current:
        for j in range(8):
            percent = random.randint(1, 100)
            number = random.randint(0, 7)
            if percent >= 98:
                i[j] = number
    return current

def diagonal(position, value ,table):
    score = 0
    n = len(table)
    for i in range(1, n):
        if position+i > 7:
            break
        if value+i > 7:
            break
        if table[position+i] == value+i:
            score += 1

    for i in range(1, n):
        if position-i < 0:
            break
        if value-i < 0:
            break
        if table[position-i] == value-i:
            score += 1
    for i in range(1, n):
        if position+i > 7:
            break
        if value+i > 7:
            break
        if table[position+i] == value-i:
            score += 1
    for i in range(1, n):
        if position-i < 7:
            break
        if value-i < 7:
            break
        if table[position-i] == value-i:
            score += 1
    return score

def fitness_fn(target):
    score = 0
    diagonal_score = 0
    collection = [0]*8
    for i in range(len(target)):
        collection[target[i]] += 1
        diagonal_score += diagonal(i, target[i], target)
    for i in collection:
        if i > 1:
            score += i-1
    return score+(diagonal_score/2)

def possibility_chart(target):
    total_fitness = 0
    chart = []
    for i in target:
        temp = fitness_fn(i)
        chart.append([fitness_max-temp, 0])
        total_fitness += fitness_max-temp
    for i in chart:
        i[1] = float(i[0]*100)/total_fitness
    return chart

def check_fitness(target):
    best = 0
    for i in range(len(target)):
        if target[i][0] == fitness_max:
            return [i, fitness_max]
        if target[i][0] > best:
            best = target[i][0]
    return [-1, best]

def search():
    current_population = []
    found_sol = False
    iteration = 0
    for i in range(population):
        current_population.append(initial_status())
    chart = possibility_chart(current_population)
    best_sol = check_fitness(chart)
    print "Initial population:"
    print current_population
    if best_sol[0] != -1:
        found_sol = True
    while(not found_sol):
        current_population = produce(current_population, chart)
        current_population = mutate(current_population)
        chart = possibility_chart(current_population)
        best_sol = check_fitness(chart)
        if best_sol[0] != -1:
            found_sol = True
        iteration += 1
        if iteration == max_iteration:
            break
        total_finess = 0
    for i in chart:
        total_finess += i[0]
    average_fitness = float(total_finess)/float(population)

    if found_sol:
        print "Solution Founded! Which is :"
        print current_population[best_sol[0]]
        print "Average fitness"
        print average_fitness
        print "Total generation:"
        print iteration
        print "final population:"
        print current_population
    else:
        print "Solution not found!"
        print "Average fitness"
        print average_fitness
        print "Total generation:"
        print iteration
        print "final population:"
        print current_population
if __name__ == "__main__":
    search()
