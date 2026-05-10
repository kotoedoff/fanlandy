# Fanland OSINT Multi-Tool

## Overview

Fanland is a powerful OSINT (Open-Source Intelligence) investigation platform with AI assistant, session management, and 11+ integrated tools for digital investigations.

## Key Features

### 🔍 OSINT Tools Integration
- **Maigret** - 3000+ sites username search
- **Sherlock** - 400+ social networks  
- **Holehe** - Email verification on 120+ sites
- **GHunt** - Google account OSINT
- **Blackbird** - 600+ sites search
- **PhoneInfoga** - Phone number intelligence
- **Toutatis** - Instagram OSINT
- **SpiderFoot** - Automated OSINT
- **theHarvester** - Email/subdomain gathering
- **WhatsMyName** - Username enumeration
- **SocialScan** - Social media checker

### 🤖 AI Assistant
- Powered by Groq (Llama 3.3 70B)
- Context-aware investigation helper
- Analyzes findings and suggests next steps
- Integrated with session data

### 📊 Session Management
- Track multiple investigations
- Store findings and connections
- Chat history with AI
- SQLite database backend

### 🎨 Modern Interface
- Customizable themes
- Background support (GIF/Video)
- Multi-language (EN/RU)
- Plugin system (Lua)

## Installation

```bash
git clone https://github.com/kotoedoff/fanlandy.git
cd fanlandy
pip install -r requirements.txt
python3 gui.py
```

## Requirements
- Python 3.11+
- PyQt6
- Groq API key (for AI assistant)
- See requirements.txt for full list

## Usage

1. Launch: `python3 gui.py`
2. Create or select investigation session
3. Use OSINT tools from categories
4. Chat with AI assistant for analysis
5. Save findings to session

## Configuration

- **Groq API Key**: Enter when first using AI assistant (saved in settings)
- **Themes**: Settings → Load/Create Theme
- **Proxy**: Settings → Network → Proxy Configuration

## License

Educational and research purposes only. See User Agreement.txt

## Credits

Original Laitoxx Multi-Tool by Asoru (@perehodasoru)  
Enhanced with AI and session management by kotoedoff
