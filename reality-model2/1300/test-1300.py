import itertools
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1)

learning_rate = 1e-1
coeffs = [.3, 0, .3, .2, .2]
unit_max = 1

class Neuron:
    def __init__(self, id):
        self.id = id
        self.state = 0
        self.prev_units = {}

neurons = [Neuron(i) for i in range(10)]
sensors = [Neuron(i) for i in range(10, 15)]
goal = Neuron(15)
#polynomy = lambda: sum([s.state * c for s, c in zip(sensors, coeffs)])
def polynomy():
    s = [sensor.state for sensor in sensors]
    return sigmoid(0.1 * s[0] ** 2 + s[1] * .35 + 0.1 * s[2] ** 3 + 0.1 * s[3] + s[4] * .35)
#polynomy = lambda: sigmoid(sum([s.state * c for s, c in zip(sensors, coeffs)]))


all_diffs = []

def init():
    '''
    for sensor in sensors:
        for neuron in neurons:
            neuron.prev_units[sensor] = random.uniform(-unit_max, unit_max)
    '''

    for sensor in sensors:
        goal.prev_units[sensor] = np.random.uniform(-unit_max, unit_max)

def set_sensors(values):
    for sensor, value in zip(sensors, values):
        sensor.state = value

def run():
    hardcoded_values = False

    for i in itertools.count():
        try:
            correct_goal, predicted_goal = do_one_step(hardcoded_values)

            all_diffs.append(abs(correct_goal - predicted_goal))
            if (i) % 2000 == 0:
                print (i)
                print (np.average([all_diffs]))

            if hardcoded_values:
                hardcoded_values = False
                print ('Diff: {}. Correct: {}. Pred: {}'.format(correct_goal - predicted_goal, correct_goal, predicted_goal))
                time.sleep(10)

        except KeyboardInterrupt:
            key = input()
            if key == 'v':
                values = [float(v) for v in input().split()]
                set_sensors(values)
                hardcoded_values = True
            elif key == 'p':
                plt.scatter(range(len(all_diffs)), all_diffs, s=.001)
                plt.show()
            elif key == 'c':
                pass

def do_one_step(hardcoded_values):
    if not hardcoded_values:
        set_sensors(np.random.uniform(0, 1, len(sensors)))
    else:
        print ('it works')
        print ([sensor.state for sensor in sensors])
        print (polynomy())
    correct_goal = polynomy()

    '''
    for neuron in neurons:
        connections = neuron.prev_units.items()
        neuron.state = sigmoid(sum([s.state * w for s, w in connections]))
    '''

    connections = goal.prev_units.items()

    predicted_goal_inv = sum([n.state * w for n, w in connections])
    predicted_goal = relu(predicted_goal_inv)
    correct_goal_inv = sigmoid_inverse(correct_goal)

    dcdsig = 1 if correct_goal > predicted_goal else -1
    dsigdpg = relu_prime(predicted_goal_inv)
    delta = learning_rate * dcdsig * dsigdpg

    #delta = learning_rate * (correct_goal_inv - predicted_goal_inv)
    for neuron, weight in goal.prev_units.items():
        goal.prev_units[neuron] += delta * neuron.state

    '''
    for neuron in neurons:
        new_delta = goal.prev_units[neuron] * delta
        for sensor, weight in neuron.prev_units.items():
            neuron.prev_units[sensor] += new_delta * sensor.state
    '''

    return correct_goal, predicted_goal

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_inverse(y):
    #if y == 0:
    return -math.log(1 / y - 1)

def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))

def relu(x):
    return max(0, x)

def relu_prime(x):
    return 1 if x > 0 else 0

init()
run()
