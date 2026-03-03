# XONICHAT 🚀

A terminal-based Gemini client optimized for low-resource devices (ASUS Eee PC, etc.)

## 📋 Description

XONICHAT is a lightweight Google Gemini client that runs entirely in the terminal. Ideal for resource-constrained devices.

## ✨ Features

- ✅ 100% terminal interface - Fast and lightweight
- ✅ Multiple API keys - Automatic switching when one is exhausted
- ✅ Conversation history - Context between messages
- ✅ Optimized - Runs on ASUS Eee PC and similar devices

## ⚙️ Quick Installation

### 1. Clone the repository
```
git clone https://github.com/xonidu/xonichat.git
cd xonichat
```

### 2. Install dependency by OS

#### 🐧 Arch Linux / Manjaro
```bash
sudo pacman -S python-pip
pip install requests --break-system-packages
```

#### 🐧 Debian / Ubuntu / antiX
```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install requests --break-system-packages
```

#### 🍎 macOS
```bash
pip3 install requests
```

#### 🪟 Windows
```bash
pip install requests
```

### 3. Configure API keys

Get your free API keys at: https://aistudio.google.com/app/apikey

Create a `keys.txt` file in the same folder with your API keys (one per line):
```
# Your Gemini API keys (one per line)
AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********
AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********
```

## 🚀 Usage

```
python start.py
# or
python3 start.py
```

- Type your message and press Enter
- Type `/salir` to exit
- The program automatically switches keys when one runs out of quota

## 📁 Files

- `start.py` - Main program
- `keys.txt` - API keys (create manually)

## 👤 Author

Darian Alberto Camacho Salas (XONIDU)

Email: xonidu@gmail.com

