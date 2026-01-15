# AI Pokemon Player

## About This Project
As a kid, I loved playing Pokémon video games. I spent countless hours exploring regions, battling trainers, and trying to catch every Pokémon. Growing up with these games left me with a continuing appreciation for the games strategy, complexity, and charm. In fact, the popularity of Pokémon (and related merchandising) has continued to grow and Pokémon is arguably now more popular than ever. Given my appreciation for machine learning and AI, I realized that combining these two interests could lead to an engaging machine learning project: Creating a Machine Learning model that is able to play Pokémon, and and ultimately beat the Pokémon champion.


# Current Progress
- [x] Virtual controller implemented in Python for sending inputs to the game
- [x] Game state capture 
- [ ] Reinforcement learning agent (planned)
- [ ] AI training loop (planned)
- [ ] Performance tracking and metrics (planned)

## Stepwise Approach / Roadmap
This project will progress in multiple stages, with each stage building on the previous one:

### **Stage 1: Basic Movement**
- Train a model that is rewarded simply for moving within the game world.
- Goal: Teach the AI basic navigation and movement mechanics.

### **Stage 2: Progression and Interaction**
- Reward the model for moving **and** interacting with NPCs (Non-playable charactrs) or objects that allow progression (e.g., talking to people, picking up items).
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
