#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICHAT 2026 - Cliente Gemini para Terminal
Optimizado para equipos de bajos recursos
Desarrollador: Darian Alberto Camacho Salas
Organización: XONIDU
"""

import os
import sys
import time
import readline
import requests
from pathlib import Path

class XONICHAT:
    def __init__(self):
        self.keys_file = self.get_keys_path()
        self.keys = []
        self.current_key_index = 0
        self.conversation_history = []
        self.max_history = 50
        self.model = "gemini-2.5-flash"
        self.api_base = "https://generativelanguage.googleapis.com/v1"
        
        self.load_keys()
        self.setup_readline()
        self.welcome()
    
    def get_keys_path(self):
        """
        Busca keys.txt en múltiples ubicaciones:
        1. Mismo directorio que xonichat.py
        2. /usr/share/xonichat/ (instalación AUR)
        3. ~/xonichat/
        4. Directorio actual
        """
        # Obtener directorio donde está este script (xonichat.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Opción 1: Mismo directorio que xonichat.py
        ruta_local = os.path.join(script_dir, 'keys.txt')
        if os.path.exists(ruta_local):
            return ruta_local
        
        # Opción 2: Instalación desde AUR
        ruta_aur = '/usr/share/xonichat/keys.txt'
        if os.path.exists(ruta_aur):
            return ruta_aur
        
        # Opción 3: Ruta fija en home del usuario
        usuario = os.path.expanduser("~")
        ruta_home = os.path.join(usuario, 'xonichat', 'keys.txt')
        if os.path.exists(ruta_home):
            return ruta_home
        
        # Opción 4: Directorio actual (donde se ejecuta)
        ruta_actual = os.path.join(os.getcwd(), 'keys.txt')
        if os.path.exists(ruta_actual):
            return ruta_actual
        
        # Si no existe, devolvemos la ruta local para crear el archivo
        return ruta_local
    
    def setup_readline(self):
        histfile = Path.home() / ".xonichat_history"
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        import atexit
        atexit.register(readline.write_history_file, histfile)
        
    def load_keys(self):
        try:
            with open(self.keys_file, 'r') as f:
                for line in f:
                    key = line.strip()
                    if key and not key.startswith('#'):
                        self.keys.append(key)
        except FileNotFoundError:
            print(f"\n[ERROR] {self.keys_file} not found")
            print("[INFO] Get your API key at: https://aistudio.google.com/app/apikey")
            print(f"[INFO] Create keys.txt in: {os.path.dirname(self.keys_file)}")
            sys.exit(1)
            
        if not self.keys:
            print("[ERROR] No valid keys in keys.txt")
            sys.exit(1)
            
    def welcome(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 60)
        print("                     XONICHAT")
        print("=" * 60)
        print(" BY: XONIDU - Darian Alberto Camacho Salas")
        print("=" * 60)
        print(f" Keys: {len(self.keys)} | Model: {self.model}")
        print(f" Keys file: {self.keys_file}")
        print("=" * 60)
        print("")
        
    def get_current_key(self):
        return self.keys[self.current_key_index]
        
    def switch_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        print(f"\n[KEY] Switching to key {self.current_key_index + 1}/{len(self.keys)}")
        
    def make_request(self, message):
        key = self.get_current_key()
        url = f"{self.api_base}/models/{self.model}:generateContent?key={key}"
        
        headers = {"Content-Type": "application/json"}
        
        contents = []
        for msg in self.conversation_history[-self.max_history:]:
            contents.append({
                "role": "user" if msg['role'] == 'user' else "model",
                "parts": [{"text": msg['content']}]
            })
        
        contents.append({
            "role": "user",
            "parts": [{"text": message}]
        })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                response_json = response.json()
                if 'candidates' in response_json and len(response_json['candidates']) > 0:
                    answer = response_json['candidates'][0]['content']['parts'][0]['text']
                    self.conversation_history.append({"role": "user", "content": message})
                    self.conversation_history.append({"role": "assistant", "content": answer})
                    return answer
                else:
                    return "[WARNING] Empty response"
                
            elif response.status_code == 429:
                print(f"\n[WARNING] Key {self.current_key_index + 1} out of quota")
                self.switch_key()
                return None
                
            elif response.status_code in [403, 404]:
                print(f"\n[ERROR] Error with key {self.current_key_index + 1}")
                if len(self.keys) > 1:
                    self.switch_key()
                return None
                
            else:
                print(f"\n[ERROR] {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("\n[TIMEOUT] Request took too long")
            return None
        except Exception as e:
            print(f"\n[ERROR] {e}")
            return None
            
    def process_command(self, cmd):
        if cmd == "/salir":
            print("\nBY: XONIDU - Darian Alberto Camacho Salas")
            print("Goodbye!")
            sys.exit(0)
        return False
        
    def run(self):
        while True:
            try:
                prompt = f"[G{self.current_key_index+1}/{len(self.keys)}] >>> "
                message = input(prompt).strip()
                
                if not message:
                    continue
                    
                if message == "/salir":
                    self.process_command(message)
                    continue
                    
                print("[...] Querying Gemini...")
                
                response = None
                attempts = 0
                max_attempts = len(self.keys) * 2
                
                while response is None and attempts < max_attempts:
                    response = self.make_request(message)
                    if response is None:
                        attempts += 1
                        time.sleep(1)
                
                if response:
                    print(f"\n[G{self.current_key_index+1}]: {response}\n")
                else:
                    print("\n[ERROR] Could not get response")
                    
            except KeyboardInterrupt:
                print("\n\nBY: XONIDU - Darian Alberto Camacho Salas")
                print("Goodbye!")
                break
            except EOFError:
                print("\n\nBY: XONIDU - Darian Alberto Camacho Salas")
                print("Goodbye!")
                break

def main():
    try:
        import requests
    except ImportError:
        print("[INFO] Installing requests...")
        os.system("pip3 install requests --break-system-packages")
        import requests
        
    # Verificar si existe keys.txt en alguna ubicación
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posibles_keys = [
        os.path.join(script_dir, 'keys.txt'),
        '/usr/share/xonichat/keys.txt',
        os.path.join(os.path.expanduser("~"), 'xonichat', 'keys.txt'),
        os.path.join(os.getcwd(), 'keys.txt')
    ]
    
    keys_exist = any(os.path.exists(p) for p in posibles_keys)
    
    if not keys_exist:
        # Crear en el directorio donde está xonichat.py
        keys_path = os.path.join(script_dir, 'keys.txt')
        with open(keys_path, 'w') as f:
            f.write("# Your Gemini API keys (one per line)\n")
            f.write("# Get them at: https://aistudio.google.com/app/apikey\n")
            f.write("\n")
            f.write("# Example:\n")
            f.write("# AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********\n")
            f.write("# AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********\n")
        print(f"\n[INFO] Created keys.txt file in: {script_dir}")
        print("       Put your API keys there and run again")
        print("       https://aistudio.google.com/app/apikey\n")
        sys.exit(0)
    
    app = XONICHAT()
    app.run()

if __name__ == "__main__":
    main()
