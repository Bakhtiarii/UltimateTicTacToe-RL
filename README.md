Ultimate Tic-Tac-Toe with Deep Reinforcement Learning:

A sophisticated implementation of Ultimate Tic-Tac-Toe using Deep Q-Network (DQN) architecture, demonstrating how reinforcement learning can master complex, hierarchical board games with nested decision spaces.

🎮 Project Overview:

Ultimate Tic-Tac-Toe transforms the classic 3×3 game into a challenging 9×9 grid composed of nine interconnected sub-boards, creating a rich strategic environment with approximately 3^81 possible configurations. This project implements an AI agent that learns to play this complex game through self-play and experience, without relying on traditional brute-force search algorithms.

🚀 Key Features:

* Custom OpenAI Gym Environment: Fully implemented Ultimate Tic-Tac-Toe environment following OpenAI Gym standards for standardized reinforcement learning
* Deep Q-Network Agent: Neural network-based agent with experience replay and epsilon-greedy exploration strategy
* Intelligent Move Validation: Enforces game-specific rules, including the unique constraint where players must play in sub-boards determined by the opponent's previous moves
* Self-Play Training: Agent improves through playing against itself, learning both tactical and strategic patterns
* Performance Metrics: Comprehensive evaluation against random players, other trained agents, and human opponents

🧠 Technical Architecture:

1- Board Implementation: NumPy-based 9×9 game state management with sub-board tracking and winner detection

2- DQN Architecture:

* 3-layer fully connected neural network
* Input: 82-dimensional vector (81 board positions + last move)
* Output: Q-values for all 81 possible actions
* Experience replay buffer for stable training


3- Training Strategy:

Epsilon-greedy exploration (ε = 1.0 → 0.01)
Discount factor γ = 0.95
Batch size of 32 for experience replay


📊 Results:

Our trained DQN agent demonstrates impressive performance:

* vs Random Players: 26 wins, 68 draws, 6 losses (26% win rate, 68% draw rate)
* vs Trained Agents: 100% draw rate, showing equally matched strategic play
* vs Human Players: 50% win rate, 50% draw rate against intermediate players
* Successfully learned to identify and block winning moves while creating strategic opportunities

🔧 Technologies Used:

* Python 3.x
* PyTorch/TensorFlow for neural network implementation
* OpenAI Gym for environment standardization
* NumPy for efficient array operations
* Experience Replay for stable Q-learning


📚 References
This project builds upon foundational work in deep reinforcement learning, particularly the DQN architecture introduced by Mnih et al. (2015) and applies it to the unique challenges of Ultimate Tic-Tac-Toe's nested game structure.
