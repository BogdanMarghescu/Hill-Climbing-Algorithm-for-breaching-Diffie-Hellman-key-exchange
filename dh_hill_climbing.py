from pandas import read_csv
from numpy.random import randn, randint
from numpy import ceil, sign
from matplotlib import pyplot as plt


def objective_function_dh(p, g, pub_key, a):
    """
    Computes the objective function for discovering one of Diffie-Hellman private keys with the hill climbing algorithm
    """
    return -abs((g ** a) % p - pub_key)


def plot_hill_climbing(p, g, pub_key, solutions, scores):
    """
    Plots the progress of the hill climbing algorithm used for discovering one Diffie-Hellman private key,
    as well as the candidate solutions of it
    """
    plt.plot(range(1, len(scores) + 1), scores, '.-')
    plt.title(f'Hill Climbing Progress for Public Key {pub_key}')
    plt.xlabel('Improvement Number')
    plt.ylabel('Evaluation f(x)')
    plt.show()
    plt.plot(range(1, p), [objective_function_dh(p, g, pub_key, x) for x in range(1, p)])
    plt.plot(solutions, scores, 'o', color='black', label='Candidate Solutions')
    plt.axvline(solutions[-1], scores[-1], ls='--', color='red', label='Best Solution')
    plt.title(f'Response Surface of Objective Function for Public Key {pub_key}')
    plt.legend(loc="upper right")
    plt.show()


def hill_climbing(p, g, pub_key, n_iterations):
    """
    Performs stochastic hill climbing search for discovering one Diffie-Hellman private key
    """
    # generate an initial point
    solution = randint(1, p)
    # evaluate the initial point
    solution_eval = objective_function_dh(p, g, pub_key, solution)
    # run the hill climb
    for i in range(n_iterations):
        # take a step
        step = randn(1)[0]
        candidate = solution + int(sign(step) * ceil(abs(step)))
        # evaluate candidate point
        candidate_eval = objective_function_dh(p, g, pub_key, candidate)
        # check if we should keep the new point
        if candidate_eval > solution_eval:
            # store the new point
            solution, solution_eval = candidate, candidate_eval
    return solution, solution_eval


def random_restarts_hill_climbing(p, g, pub_key, n_iterations, n_restarts=None):
    """
    Performs the hill climbing search with random restarts for discovering one Diffie-Hellman private key - infinite
    number of restarts if n_restarts is None
    """
    best, best_eval = None, -p
    n = 0
    solutions = []
    scores = []
    while best_eval < 0:
        if n_restarts is not None and n >= n_restarts:
            break
        # perform a stochastic hill climbing search
        solution, solution_eval = hill_climbing(p, g, pub_key, n_iterations)
        # check for new best
        if solution_eval > best_eval:
            best, best_eval = solution, solution_eval
            # report progress
            print(f'Restart {n}, best: f({best}) = {best_eval}')
            solutions.append(solution)
            scores.append(solution_eval)
        n += 1
    return best, best_eval, solutions, scores


def diffie_hellman_hill_climbing(p, g, A, B, n_iterations, n_restarts=None):
    """
    Performs the hill climbing search with random restarts for breaching Diffie-Hellman key exchange - infinite number
    of restarts if n_restarts is None
    """
    print(f"We will breach the Diffie-Hellman key exchange cipher with the following public parameters: p = {p}, g = {g}, A = {A}, B = {B}")
    print("\nDiscovering the first private key:")
    best_a, score_a, solutions_a, scores_a = random_restarts_hill_climbing(p, g, A, n_iterations, n_restarts)
    plot_hill_climbing(p, g, A, solutions_a, scores_a)
    print("\nDiscovering the second private key:")
    best_b, score_b, solutions_b, scores_b = random_restarts_hill_climbing(p, g, B, n_iterations, n_restarts)
    plot_hill_climbing(p, g, B, solutions_b, scores_b)
    return best_a, best_b, score_a, score_b


dh_data = read_csv("dh_values.csv")
dh_index = 3
p, g, A, B = dh_data.iloc[dh_index]
# best_a, best_b, score_a, score_b = diffie_hellman_hill_climbing(p, g, A, B, n_iterations=100, n_restarts=1000)  # for finite number of restarts
best_a, best_b, score_a, score_b = diffie_hellman_hill_climbing(p, g, A, B, n_iterations=100)
print(f"\nDiffie-Hellman key exchange breach results for public parameters p = {p}, g = {g}, A = {A}, B = {B}:\na = {best_a}\nb = {best_b}")
print(f'f({best_a}) = {score_a}')
print(f'f({best_b}) = {score_b}')
