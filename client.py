import connection as cn
from random import random, randint
import time

s = cn.connect(2037)

def q_update(state, action, reward, next_state):
    alpha = 0.6
    gamma = 0.4

    action = 0 if action == 'left' else 1 if action == 'right' else 2

    print(f'last_qvalue: {qtable[state][action]}')

    qtable[state][action] = (1 - alpha) * qtable[state][action] + alpha * (reward + gamma * max(qtable[next_state]))

    print(f'new_qvalue: {qtable[state][action]}')

death = -100
win = 300

while True:
    state = 0
    new_state = 0
    reward = 0

    file = open('resultado.txt', 'r')
    file_content = file.readlines()
    file.close()

    qtable = []

    for line in file_content:
        line = line.split()
        for i in range(len(line)):
            line[i] = float(line[i])

        qtable.append(line)

    while not reward == win:
        state = new_state

        actions = {0: 'left', 1: 'right', 2: 'jump'}

        if random() < 0.1:
            action_idx = randint(0, 2)
            
        else: 
            action_idx = qtable[state].index(max(qtable[state]))    
        
        action = actions[action_idx]
        
        new_state, reward = cn.get_state_reward(s, action)

        new_state = int(str(new_state), 2)

        print(f'state: {state}, action: {action},  new_state: {new_state}, reward: {reward}')

        q_update(state, action, reward, new_state)

        if (reward == death):
            print('Morreu')
            break

        if (reward == win):
            print('Ganhou')

    visited_states = []

    file = open('resultado.txt', 'w')

    content = ''

    for line in qtable:
        for (i, value) in enumerate(line):
            line[i] = str(value)

        content += ' '.join(line) + '\n'

    file.write(content)

    time.sleep(3)


