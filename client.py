import connection as cn
import time

s = cn.connect(2037)

# visited_states = []

def bin_to_dec(num):
    print(num)
    return int(num.replace('0b', ""), 2)

def q_update(state, action, reward, next_state):
    alpha = 0.6
    gamma = 0.4

    action = 0 if action == 'left' else 1 if action == 'right' else 2

    # if (len(visited_states) > 16): visited_states = visited_states[-16:]

    # if (visited_states.count(state) > 2): 
    #     reward = reward * 1.5
    # else:
    #     visited_states.append(state)

    # print(visited_states)

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

        action = qtable[state].index(max(qtable[state]))
        action = 'left' if action == 0 else 'right' if action == 1 else 'jump'
        
        new_state, reward = cn.get_state_reward(s, action)

        new_state = int(str(new_state), 2)

        # print(f'state: {state}, action: {action},  new_state: {new_state}, reward: {reward}')

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


