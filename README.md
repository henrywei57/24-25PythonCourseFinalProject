# 🎮 Blackjack Game

A modern implementation of the classic casino card game Blackjack, developed using Python and Pygame. This project combines traditional Blackjack rules with engaging visual elements and interactive features.

![Blackjack Game](https://via.placeholder.com/800x400?text=Blackjack+Game+Screenshot)

## 🎯 Features

- Modern UI with animated card reveals and dealer interactions
- Interactive betting system with balance management
- Engaging visual feedback for game events
- Bonus video reward system for extended gameplay
- Dynamic quit button that evades the cursor
- Persistent balance tracking
- Fullscreen video rewards

## 🛠️ Technology Stack

### Libraries
- `pygame`: Core game engine and graphics
- `cv2`: Video playback functionality
- `random`: Card shuffling and random selection
- `math`: Mathematical calculations for animations
- `threading`: Concurrent operations

### Development Tools
- Visual Studio Code: Primary IDE
- Git: Version control
- Python 3.x: Programming language

## 📋 Project Structure
```
project/
├── main.py              # Main game logic
├── money_manager.py     # Balance management
├── video1.mp4          # Reward videos
├── video2.mp4
├── video3.mp4
├── video4.mp4
└── video5.mp4
```

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Pygame
- OpenCV (cv2)

### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/blackjack-game.git
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Run the game
```bash
python main.py
```

## 🎲 Game Rules

- Standard Blackjack rules apply
- Blackjack pays 3:2
- Dealer must hit on soft 17
- Double down and split not implemented in current version
- Watch videos to earn bonus credits!

## 💻 Development

### Main Components
1. Game Initialization
   - Pygame setup
   - Screen configuration
   - Font initialization
   - Balance loading

2. Core Game Logic
   - Card management
   - Player/Dealer hand management
   - Betting system
   - Game state management

3. User Interface
   - Card rendering
   - Button interactions
   - Balance display
   - Message system

4. Special Features
   - Video reward system
   - Dynamic quit button
   - Balance persistence

### Code Origin
- Self-written code: ~70%
  - Core game logic
  - Card management
  - Player/Dealer classes
  - Basic UI elements

- AI-assisted code: ~30%
  - Complex animations
  - Video integration
  - Dynamic quit button
  - Advanced UI features

## 🔮 Future Improvements

1. Enhanced Features
   - Multiplayer support
   - Card counting practice mode
   - Strategy advisor
   - Tournament mode

2. Technical Improvements
   - Performance optimization
   - Mobile platform support
   - Online leaderboards
   - Enhanced graphics

3. Educational Additions
   - Tutorial system
   - Strategy guides
   - Statistics tracking
   - Learning resources

## 📝 Development Challenges & Solutions

1. Card Animation Synchronization
   - Solution: Implemented timing system for card reveals
   - Learning: Importance of state management in animations

2. Balance Persistence
   - Solution: Created separate money manager module
   - Learning: Data persistence in game applications

3. Video Integration
   - Solution: Used OpenCV for video playback
   - Learning: External library integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Thanks to the Pygame community for their excellent documentation
- OpenCV for video playback capabilities
- All contributors and testers

## 📞 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/blackjack-game](https://github.com/yourusername/blackjack-game) 