# AI Pokemon Player

## About This Project
Ever since I was a kid, I’ve loved playing Pokémon video games. I spent countless hours exploring regions, battling trainers, and trying to catch every Pokémon. Growing up with these games left me with a deep appreciation for their strategy, complexity, and charm.  

At the same time, I’ve always been fascinated by machine learning and AI — how algorithms can learn, adapt, and constantly improve. I realized that combining these two passions could lead to a project I’m truly excited about: teaching an AI to play Pokémon… and eventually beat it.  

This project is my attempt at that. So far, I’ve built a virtual controller in Python that allows a programmatic interface to the game, laying the groundwork for a machine learning agent to take control.


# Current Progress
- [x] Virtual controller implemented in Python for sending inputs to the game
- [ ] Game state capture (planned)
- [ ] Reinforcement learning agent (planned)
- [ ] AI training loop (planned)
- [ ] Performance tracking and metrics (planned)

## Stepwise Approach / Roadmap
This project will progress in multiple stages, with each stage building on the previous one:

### **Stage 1: Basic Movement**
- Train a model that is rewarded simply for moving within the game world.
- Goal: Teach the AI basic navigation and movement mechanics.

### **Stage 2: Progression and Interaction**
- Reward the model for moving **and** interacting with NPCs or objects that allow progression (e.g., talking to people, picking up items).
- Goal: Teach the AI to explore the game world and make meaningful progress.

### **Stage 3: Catching and Training Pokémon**
- Reward the model for catching Pokémon, training them, and building a team.
- Goal: Combine movement, interaction, and early team-building strategies.

### **Stage 4: Full Game Strategy**
- Train a final model that incorporates all previous stages.
- Reward system based on battles won:
  - Standard trainers: small reward
  - Gym Leaders: medium reward
  - Elite Four: large reward
  - Champion: ultimate reward
- Goal: Build a fully trained AI capable of defeating the Pokémon Champion, leveraging knowledge from all prior stages.
