import pandas as pd
import numpy as np
import time
import random

# Global variables
ACTIONS = ['up', 'down', 'left', 'right']
LENGTH = 3
N_STATES = LENGTH * LENGTH  # 9 space environment (3x3 matrix)
TERMINAL = (2, 1)
EPSILON = None
MAX_EPISODE = 500
GAMMA = None
ALPHA = None
START = None
HOLE1 = None
HOLE2 = None
TERMINAL = None
EPSILON = None
MAX_EPISODE = None
GAMMA = None
ALPHA = None
FIRST = True


def build_q_table():
    # build Q table, initialized to zero, with states as rows (9) and all possible actions as columns (4)
    global N_STATES
    global ACTIONS
    table = pd.DataFrame(
        np.zeros((N_STATES, len(ACTIONS))),
        columns=ACTIONS
    )
    return table


def actor(observation, q_table):
    if np.random.uniform() < EPSILON:
        state_action = q_table.loc[observation, :]
        # action choice
        action = np.random.choice(
            state_action[state_action == np.max(state_action)].index)
    else:
        action = np.random.choice(ACTIONS)
    return action


def init_env(robot_start, robot_end):
    global HOLE1
    global HOLE2
    global FIRST
    global START
    global TERMINAL
    HOLE1 = (1, 0)
    HOLE2 = (1, 1)
    TERMINAL = robot_end
    START = robot_start
    start = START
    FIRST = False
    return start, False


def get_env_feedback(state, action):
    reward = 0.
    end = False
    a, b = state

    if action == 'up':
        a -= 1  # change the state according to the action choice
        if a < 0:
            a = 0
        next_state = (a, b)  # update the state according to the action choice
        if next_state == TERMINAL:
            reward = 1.
            end = True
        elif (next_state == HOLE1) or (next_state == HOLE2):
            reward = -1.  # negative reward if the obstacle has been hit
            end = True

    elif action == 'down':
        a += 1
        if a >= LENGTH:
            a = LENGTH - 1
        next_state = (a, b)
        if next_state == TERMINAL:
            reward = 1.
            end = True
        if (next_state == HOLE1) or (next_state == HOLE2):
            reward = -1.
            end = True

    elif action == 'left':
        b -= 1
        if b < 0:
            b = 0
        next_state = (a, b)
        if next_state == TERMINAL:
            reward = 1.
            end = True
        if (next_state == HOLE1) or (next_state == HOLE2):
            reward = -1.
            end = True

    elif action == 'right':
        b += 1
        if b >= LENGTH:
            b = LENGTH - 1
        next_state = (a, b)
        if next_state == TERMINAL:
            reward = 1.
            end = True
        elif (next_state == HOLE1) or (next_state == HOLE2):
            reward = -1.
            end = True

    return next_state, reward, end


def playGame(q_table):
    maze_transitions = []
    waypoints = []
    state = (1, 2)  # START POINT
    end = False
    LENGTH = 3
    a, b = state
    i = 0
    
    while not end:
        act = actor(a * LENGTH + b, q_table)  # choice of the action that mazimize the state of the q_table
        print("step:", i, " action:", act)
        maze_transitions.append(act)  # copy of all the action choice
        next_state, reward, end = get_env_feedback(state, act)
        state = next_state
        waypoints.append(state)  # copy of all states from start to end
        a, b = state
        i += 1
    return maze_transitions, waypoints


# Qlearning algoritm
def Qlearn(max_episode, robot_start, robot_end):
    MAX_EPISODE = max_episode
    q_table = build_q_table()
    episode = 0
    while episode < MAX_EPISODE:
        state, end = init_env(robot_start, robot_end)
        step = 0
        while not end:
            a, b = state

            # (a * LENGTH + b) -> position of the actor in the matrix 3x3
            # return the action from the actor
            act = actor(a * LENGTH + b, q_table)

            next_state, reward, end = get_env_feedback(state, act)

            na, nb = next_state

            q_predict = q_table.loc[a * LENGTH + b, act]

            if next_state != TERMINAL:
                q_target = reward + GAMMA * \
                    q_table.iloc[na * LENGTH + nb].max()
            else:
                q_target = reward
            q_table.loc[a * LENGTH + b, act] += ALPHA * (q_target - q_predict)
            state = next_state
            step += 1

        episode += 1
    return q_table


def run_brain():
    LENGTH = 3
    N_STATES = LENGTH * LENGTH
    global EPSILON
    global GAMMA
    global ALPHA
    global MAX_EPISODE
    EPSILON = 0.9  # .95
    MAX_EPISODE = 500  # 200
    GAMMA = 0.95  # 0.9
    ALPHA = 0.01  # 0.001, 0.002
    robot_start = (1, 2)
    robot_end = (2, 1)

    q_table = Qlearn(MAX_EPISODE, robot_start, robot_end)
    print(q_table)  # q learning table
    maze_transitions, waypoints = playGame(q_table)  # actions taken by agent to reach the goal
    return waypoints
