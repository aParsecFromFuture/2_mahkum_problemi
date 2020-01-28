from include.NeuralNetwork import *


def run(prison_1, prison_2):
    prison_1_alive = True
    prison_2_alive = True
    prison_1_health = 3
    prison_2_health = 3

    did_prison_1_feed = False
    did_prison_2_feed = False
    then_prison_1_feed = False
    then_prison_2_feed = False

    then_prison_1_feed_next = False
    then_prison_2_feed_next = False

    score_1 = 0
    score_2 = 0

    while prison_1_alive or prison_2_alive:
        if prison_1_health == 0:
            prison_1_alive = False
        if prison_2_health == 0:
            prison_2_alive = False

        if prison_1_alive:
            score_1 = score_1 + 1
            output = np.argmax(prison_1.get_output([did_prison_2_feed, did_prison_1_feed, then_prison_2_feed])[0])
            if output == 0:
                prison_2_health = 3
                then_prison_1_feed_next = True
            if output == 1:
                prison_2_alive = False
            if output == 2:
                then_prison_1_feed_next = False

        if prison_2_alive:
            score_2 = score_2 + 1
            output = np.argmax(prison_2.get_output([did_prison_1_feed, did_prison_2_feed, then_prison_1_feed])[0])
            if output == 0:
                prison_1_health = 3
                then_prison_2_feed_next = True
            if output == 1:
                prison_1_alive = False
            if output == 2:
                then_prison_2_feed_next = False

        if score_1 >= 50 or score_2 >= 50:
            break

        prison_1_health = prison_1_health - 1
        prison_2_health = prison_2_health - 1

        did_prison_1_feed = then_prison_1_feed
        did_prison_2_feed = then_prison_2_feed

        then_prison_1_feed = then_prison_1_feed_next
        then_prison_2_feed = then_prison_2_feed_next

    return [score_1, score_2]


def generate_population(parent, generation_size):
    population = []
    for i in range(generation_size):
        child = NeuralNetwork(3, [5, 3])

        mutation_matrix = np.random.uniform(size=parent.weights[0].shape)
        child.weights[0] = parent.weights[0] + mutation_matrix
        mutation_matrix = np.random.uniform(size=parent.bias[0].shape)
        child.bias[0] = parent.bias[0] + mutation_matrix

        mutation_matrix = np.random.uniform(size=parent.weights[1].shape)
        child.weights[1] = parent.weights[1] + mutation_matrix
        mutation_matrix = np.random.uniform(size=parent.bias[1].shape)
        child.bias[1] = parent.bias[1] + mutation_matrix

        population.append(child)
    return population


POPULATION_SIZE = 2
GENERATION_COUNT = 10

prison_A = NeuralNetwork(3, [5, 3])
prison_B = NeuralNetwork(3, [5, 3])

best_score_A = -1
best_child_A = prison_A
best_score_B = -1
best_child_B = prison_B

for generation in range(GENERATION_COUNT):
    population_A = generate_population(best_child_A, POPULATION_SIZE)
    population_B = generate_population(best_child_B, POPULATION_SIZE)
    for child_A in population_A:
        for child_B in population_B:
            score = run(child_A, child_B)
            if best_score_A < score[0]:
                best_child_A, best_score_A = child_A, score[0]
            if best_score_B < score[1]:
                best_child_B, best_score_B = child_B, score[1]
    print("score A : " + str(best_score_A) + " score B : " + str(best_score_B))
