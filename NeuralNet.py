import numpy as np

mutation_rate = 0.2
mutation_range = 1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class NeuralNetwork:
    def __init__(self, input, hidden, output):
        # self.input      = np.zeros((1, 3))
        self.input_layers = input
        self.hidden_layers = hidden
        self.output_layers = output
        self.weights = 2 * np.random.random(((input + output) * hidden, 1)) - 1
        self.output = np.zeros((1, 1))
        self.distance = 0

    def feedforward(self, x):
        weights1 = self.weights[:(self.input_layers*self.hidden_layers)]
        weights1 = np.reshape(weights1, (self.input_layers, self.hidden_layers))

        weights2 = self.weights[(self.input_layers*self.hidden_layers):]
        weights2 = np.reshape(weights2, (self.hidden_layers, self.output_layers))

        layer1 = sigmoid(np.dot(x, weights1))
        # z = np.ones((layer1.shape[0], 1))
        # layer1 = np.hstack((z, layer1))
        self.output = sigmoid(np.dot(layer1, weights2))
        # print(self.output[0][0])
        return self.output[0][0]

    def mutate(self):
        for weight in self.weights:
            if np.random.rand() <= mutation_rate:
                weight += np.random.rand() * mutation_range * 2 - mutation_range





# initialize(5)
# fitness(np.array([1, 2, 3, 4, 5]))
# for bird in birds:
#     print(bird.distance, bird.output)
