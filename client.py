import connection as cn
import time
import random

s = cn.connect(2037)

def q_update(state, action, reward, next_state, qtable, alpha, gamma):
    actions = {'left': 0, 'right': 1, 'jump': 2}
    action_idx = actions[action]

    new_qvalue = (1 - alpha) * qtable[state][action_idx] + alpha * (reward + gamma * max(qtable[next_state]))
    qtable[state][action_idx] = new_qvalue

    return qtable

death_reward = -100
win_reward = 300
epsilon = 0.2
alpha = 0.3
gamma = 0.7

while True:
    state = 27
    new_state = 0
    reward = 0

    with open('resultado.txt', 'r') as f:
        qtable = [[float(q) for q in line.split()] for line in f.readlines()]

    while not reward == win_reward:
        if random.random() < epsilon:
            action_idx = random.choice([0, 1, 2])
        else:
            action_idx = qtable[state].index(max(qtable[state]))

        actions = {0: 'left', 1: 'right', 2: 'jump'}
        action = actions[action_idx]

        new_state, reward = cn.get_state_reward(s, action)
        new_state = int(new_state, 2)

        qtable = q_update(state, action, reward, new_state, qtable, alpha, gamma)

        state = new_state

        if reward == death_reward:
            print('Morreu')
            break
        elif reward == win_reward:
            print('Ganhou')
            break

    with open('resultado.txt', 'w') as f:
        for line in qtable:
            f.write(' '.join(str(q) for q in line) + '\n')

    time.sleep(2.5)