
Built by https://www.blackbox.ai

---

```markdown
# Future MT5 - Trading Automation Platform

## Project Overview
Future MT5 is a trading automation application built for the MetaTrader 5 platform. The application allows users to create and manage trading strategies, including advanced techniques like moving averages and head & shoulders pattern detection. It features a modern user interface built with Tkinter and incorporates safe credential management for user logins.

## Installation
To get started with Future MT5, follow these installation steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/future-mt5.git
   cd future-mt5
   ```

2. **Install required packages**:
   Make sure you have Python 3 installed. Install the necessary Python packages using:
   ```bash
   pip install MetaTrader5 cryptography
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage
- **Launch**: Start the application using the command mentioned above. The application will display a splash screen followed by a login window.
- **Login**: Enter your MetaTrader 5 server, account login, and password.
- **Set Up Strategy**: Once logged in, configure your trading parameters by accessing the advanced settings.
- **Automated Trading**: The application will use the defined trading strategies to manage trades automatically based on market data.

## Features
- **User-friendly Interface**: Modern UI designed using Tkinter for a pleasant user experience.
- **Trading Strategies**: Implement and use various trading strategies, including Future Breakout using moving averages and chart pattern detection.
- **Safe Credential Management**: Secure storage for your MT5 login details using encryption.
- **Logging**: Detailed logging of application activities for easier debugging and monitoring.
- **Configuration Options**: Customizable trading parameters such as break-even settings, trailing stops, and daily profit targets.

## Dependencies
The application relies on the following libraries:
- `MetaTrader5`: For trading functionalities.
- `cryptography`: For secure handling of user credentials.
- `tkinter`: For the graphical user interface.

These can be installed via pip as mentioned in the installation section.

## Project Structure
```
future-mt5/
│
├── estrategia.py         # Contains the trading strategy classes.
├── main.py               # Entry point of the application.
├── login.py              # User login interface and functionality.
├── splash_screen.py      # Splash screen implementation with animations.
├── utils.py              # Utility functions for logging, themes, and security.
├── configuracoes_avancadas.py  # Configuration settings for trading options.
│
├── requirements.txt      # List of dependencies for installation.
└── README.md             # Project documentation.
```
```
This README provides a clear overview of the project, its setup, usage instructions, key features, dependencies, and `Project Structure`. Adjust the repository URL in the installation section and any details specific to your environment as necessary.