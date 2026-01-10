import pickle
from pyboy import PyBoy
from pyboy.utils import WindowEvent, PyBoyInvalidInputException

# ------------------------------
# Controller Functions
# ------------------------------
def button(pyboy, input, hold_frames=5):
    input = input.lower()
    mapping = {
        "left": (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT),
        "right": (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT),
        "up": (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP),
        "down": (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN),
        "a": (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A),
        "b": (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B),
        "start": (WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START),
        "select": (WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT),
    }
    if input not in mapping:
        raise PyBoyInvalidInputException("Unrecognized input:", input)

    press, release = mapping[input]
    pyboy.send_input(press)
    for _ in range(hold_frames):
        pyboy.tick()
    pyboy.send_input(release)

def advance(pyboy, frames=60):
    for _ in range(frames):
        pyboy.tick()

# ------------------------------
# Load ROM
# ------------------------------
rom_path = r"C:\Users\rkemp\Downloads\Pokemon_ Red Version\Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb"
pyboy = PyBoy(rom_path)
pyboy.set_emulation_speed(8)

# ------------------------------
# Boot & Intro Sequence
# ------------------------------

# Title screen
advance(pyboy, 1500)
button(pyboy, "start", hold_frames=15)
advance(pyboy, 120)
button(pyboy, "start", hold_frames=15)
advance(pyboy, 120)

# Professor Oak Dialogue
for _ in range(13):
    advance(pyboy, 180)
    button(pyboy, "a", hold_frames=15)
advance(pyboy, 180)

# Picking Player Name
button(pyboy, "down", hold_frames=45)
advance(pyboy, 100)
button(pyboy, "a", hold_frames=15)
advance(pyboy, 180)

# Picking Rival Name
for _ in range(5):
    advance(pyboy, 180)
    button(pyboy, "a", hold_frames=15)
advance(pyboy, 180)
button(pyboy, "a", hold_frames=5)
advance(pyboy, 120)
button(pyboy, "down", hold_frames=15)
advance(pyboy, 60)

# Sequence after rival name
for _ in range(10):
    advance(pyboy, 180)
    button(pyboy, "a", hold_frames=15)

#Getting to movement
for _ in range(3):
    advance(pyboy, 180)
    button(pyboy, "a", hold_frames=15)
print("Reached first playable tile!")

# --------------------------------------------------
#Memory Reader
PLAYER_Y = 0xD361
PLAYER_X = 0xD362
MAP_ID   = 0xD35E

def get_player_position(pyboy):
    x = pyboy.memory[PLAYER_X]
    y = pyboy.memory[PLAYER_Y]
    map_id = pyboy.memory[MAP_ID]
    return x, y, map_id

x, y, map_id = get_player_position(pyboy)
print("Player position:", x, y, map_id)
# --------------------------------------------------

# Stage 1: Exploring the world (improved)
class PokemonEnvStage1:
    """
    Stage 1: Basic movement environment.
    Rewards the agent for moving to new tiles and exploring new maps.
    """
    def __init__(self, pyboy, use_visited=True):
        self.pyboy = pyboy
        self.last_position = None
        self.last_map_id = None
        self.use_visited = use_visited
        self.visited = set() if use_visited else None
        self.maps_visited = set()  # track which maps have been visited

    def step(self, action):
        # Press the button and advance frames (faster for learning)
        button(self.pyboy, action, hold_frames=5)
        advance(self.pyboy, 20)

        # Get current state
        x, y, map_id = get_player_position(self.pyboy)
        reward = 0

        # Reward for visiting new tiles
        if self.use_visited:
            if (x, y, map_id) not in self.visited:
                reward += 1
                self.visited.add((x, y, map_id))
                self.last_position = (x, y)
            else:
                # Optional tiny penalty for revisiting a tile
                reward -= 0.05
        else:
            if self.last_position is None:
                self.last_position = (x, y)
            elif (x, y) != self.last_position:
                reward += 1
                self.last_position = (x, y)
            else:
                reward -= 0.05  # penalty for staying in the same spot

        # Bonus reward for entering a new map
        if map_id != self.last_map_id and map_id not in self.maps_visited:
            reward += 3  # bonus for exploring a new map
            self.maps_visited.add(map_id)

        self.last_map_id = map_id  # update for next step
        done = False  # Stage 1 never ends
        return (x, y, map_id), reward, done

    def reset(self):
        # Reset the environment
        x, y, map_id = get_player_position(self.pyboy)
        self.last_position = (x, y)
        self.last_map_id = map_id
        if self.use_visited:
            self.visited = set([(x, y, map_id)])
        self.maps_visited = set([map_id])
        return (x, y, map_id)

#------------------------------------------------------------

#Stage 1 Agent Prototype Test

import random

# Define possible movement actions
actions = ["up", "down", "left", "right"]

# Initialize Stage 1 environment
env = PokemonEnvStage1(pyboy, use_visited=True)
state = env.reset()
print("Starting position:", state)

#--------------------------------------------------------
#Q-learning
num_episodes = 100  # run 100 instances
max_steps = 50      # max steps per episode

# Initialize Q-table
q_table = {}

for episode in range(num_episodes):
    state = env.reset()  # start a new episode
    for step in range(max_steps):
        # Choose action (epsilon-greedy)
        if state not in q_table:
            q_table[state] = {a: 0 for a in actions}
        epsilon = 0.3
        if random.random() < epsilon:
            action = random.choice(actions)
        else:
            # Pick best known action
            action = max(q_table[state], key=q_table[state].get)

        next_state, reward, done = env.step(action)

        # Initialize next state in Q-table
        if next_state not in q_table:
            q_table[next_state] = {a: 0 for a in actions}

        # Q-learning update
        alpha = 0.1
        gamma = 0.9
        q_table[state][action] += alpha * (reward + gamma * max(q_table[next_state].values()) - q_table[state][action])

        state = next_state

# At the end of each episode
print(f"Episode {episode+1}: visited {len(env.visited)} unique tiles")

#------------------------------------------------------------------------
# Save the Q-table
with open("stage1_qtable.pkl", "wb") as f:
    pickle.dump(q_table, f)

# Load the Q-table later
with open("stage1_qtable.pkl", "rb") as f:
    q_table = pickle.load(f)

#--------------------------------------------------------
with open("stage1_qtable.pkl", "rb") as f:
    loaded_q_table = pickle.load(f)
print(type(loaded_q_table))  # should be <class 'dict'>
print(len(loaded_q_table))  # number of states stored
print(q_table == loaded_q_table)  # should print True
for state, actions in list(loaded_q_table.items())[:5]:
    print(state, actions)
    

