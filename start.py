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
        """Busca keys.txt priorizando ~/.xonichat/ (sin sudo)"""
        
        # Opción 1: Directorio en HOME (recomendado, sin sudo)
        home_keys = os.path.join(os.path.expanduser("~"), '.xonichat', 'keys.txt')
        if os.path.exists(home_keys):
            return home_keys
        
        # Opción 2: Mismo directorio que xonichat.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_keys = os.path.join(script_dir, 'keys.txt')
        if os.path.exists(local_keys):
            return local_keys
        
        # Opción 3: /usr/share/xonichat/ (legacy)
        system_keys = '/usr/share/xonichat/keys.txt'
        if os.path.exists(system_keys):
            return system_keys
        
        # Opción 4: ~/xonichat/ (legacy)
        home_legacy = os.path.join(os.path.expanduser("~"), 'xonichat', 'keys.txt')
        if os.path.exists(home_legacy):
            return home_legacy
        
        return home_keys
    
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
            print(f"\n[ERROR] No se encuentra keys.txt")
            print("[INFO] Obten tu API key en: https://aistudio.google.com/app/apikey")
            print(f"[INFO] Crea keys.txt en: {os.path.dirname(self.keys_file)}")
            sys.exit(1)
            
        if not self.keys:
            print("[ERROR] No hay keys validas en keys.txt")
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
        print(f"\n[KEY] Cambiando a key {self.current_key_index + 1}/{len(self.keys)}")
        
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
                    return "[WARNING] Respuesta vacia"
                
            elif response.status_code == 429:
                print(f"\n[WARNING] Key {self.current_key_index + 1} sin cuota")
                self.switch_key()
                return None
                
            elif response.status_code in [403, 404]:
                print(f"\n[ERROR] Error con key {self.current_key_index + 1}")
                if len(self.keys) > 1:
                    self.switch_key()
                return None
                
            else:
                print(f"\n[ERROR] {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("\n[TIMEOUT] La peticion tardo demasiado")
            return None
        except Exception as e:
            print(f"\n[ERROR] {e}")
            return None
            
    def process_command(self, cmd):
        if cmd == "/salir":
            print("\nBY: XONIDU - Darian Alberto Camacho Salas")
            print("Hasta luego!")
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
                    
                print("[...] Consultando Gemini...")
                
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
                    print("\n[ERROR] No se pudo obtener respuesta")
                    
            except KeyboardInterrupt:
                print("\n\nBY: XONIDU - Darian Alberto Camacho Salas")
                print("Hasta luego!")
                break
            except EOFError:
                print("\n\nBY: XONIDU - Darian Alberto Camacho Salas")
                print("Hasta luego!")
                break

def main():
    try:
        import requests
    except ImportError:
        print("[INFO] Instalando requests...")
        os.system("pip3 install requests --break-system-packages")
        import requests
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posibles_keys = [
        os.path.join(os.path.expanduser("~"), '.xonichat', 'keys.txt'),
        os.path.join(script_dir, 'keys.txt'),
        '/usr/share/xonichat/keys.txt',
        os.path.join(os.path.expanduser("~"), 'xonichat', 'keys.txt'),
        os.path.join(os.getcwd(), 'keys.txt')
    ]
    
    keys_exist = any(os.path.exists(p) for p in posibles_keys)
    
    if not keys_exist:
        home_dir = os.path.join(os.path.expanduser("~"), '.xonichat')
        os.makedirs(home_dir, exist_ok=True)
        keys_path = os.path.join(home_dir, 'keys.txt')
        with open(keys_path, 'w') as f:
            f.write("# Tus API keys de Gemini (una por linea)\n")
            f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n\n")
            f.write("# Ejemplo:\n")
            f.write("# AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********\n")
            f.write("# AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********\n")
        print(f"\n[INFO] Creado keys.txt en: {keys_path}")
        print("       Agrega tus API keys y vuelve a ejecutar")
        print("       https://aistudio.google.com/app/apikey\n")
        sys.exit(0)
    
    app = XONICHAT()
    app.run()

if __name__ == "__main__":
    main()
