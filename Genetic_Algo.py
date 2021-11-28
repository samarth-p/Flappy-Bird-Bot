import random

import numpy as np

from NeuralNet import NeuralNetwork

birds = []
next_gen = []
num_birds = 0

input_layers = 2
hidden_layers = 6
output_layers = 1


def print_weight(birdz):
    for bird in birdz:
        weights1 = bird.weights[:(bird.input_layers * bird.hidden_layers)]
        weights1 = np.reshape(weights1, (bird.input_layers, bird.hidden_layers))
        print(weights1)


def initialize(n_birds):
    global birds
    global num_birds
    num_birds = n_birds
    for i in range(n_birds):
        bird = NeuralNetwork(input_layers, hidden_layers, output_layers)
        birds.append(bird)
    # print_weight(birds)


def flappy_boi(x1, x2, i):
    x = np.array([[x1, x2]])
    y = birds[i].feedforward(x)
    return y


def fitness(dist):
    # function to copy the distance travelled (fitness function) of each bird to its neural network class
    for i, bird in enumerate(birds):
        bird.distance = dist[i]
        # print(bird.distance)


def crossover(parent1, parent2):
    # initialize child neural network
    # child get the weights from both parents
    # crossover factor is 0.5
    child = NeuralNetwork(input_layers, hidden_layers, output_layers)
    for i in range(len(child.weights)):
        child.weights[i] = random.choice([parent1.weights[i], parent2.weights[i]])

    # apply some mutation to the child
    child.mutate()
    return child


def selection():
    # sort birds according to their fitness (distance travelled)
    global birds
    birds.sort(key=lambda x: x.distance, reverse=True)
    # print('\n')
    # for bird in birds:
        # print(bird.distance)

    # 40% of top performing birds are retained for the next generation
    retain_num = int(np.ceil(0.2 * num_birds))
    global next_gen
    next_gen = birds[:retain_num]
    # print_weight(next_gen)
    # print('1\n')

    for i in range(int(np.ceil(0.1 * num_birds))):
        new_bird = NeuralNetwork(input_layers, hidden_layers, output_layers)
        next_gen.append(new_bird)

    # randomly select some lesser fit birds with a chance of 10%
    for bird in birds[retain_num:]:
        if np.random.rand() <= 0.1:
            next_gen.append(bird)

    # print_weight(next_gen)
    # print('3\n')

    # Breeding time
    # calculate number of children needed for next generation
    next_gen_len = len(next_gen)
    num_child = len(birds) - next_gen_len
    # print("num_child = " + str(num_child))
    while num_child:

        # select any 2 parents from next_gen list
        i = np.random.randint(0, next_gen_len)
        j = np.random.randint(0, next_gen_len)
        # print('yo' + str(i) + str(j))
        # breed them and send to next generation list
        if i != j:
            parent1 = next_gen[i]
            parent2 = next_gen[j]
            child = crossover(parent1, parent2)
            next_gen.append(child)
            num_child -= 1
            # print("num_child = " + str(num_child))
            # print_weight(next_gen)
            # print('\n')
    # print('\n')
    # print_weight(next_gen)
    # print('\n')

    # replace birds list with next generation
    birds = next_gen
    next_gen = []


# testing
# initialize(5)
# selection()














