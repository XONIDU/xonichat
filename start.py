#!/usr/bin/env python3
"""
XONICHAT - Cliente Gemini para terminal
Version sin limites de respuesta
BY: XONIDU - Darian Alberto Camacho Salas
"""

import os
import sys
import time
import readline
import requests
from pathlib import Path

class XONICHAT:
    def __init__(self):
        self.keys_file = "keys.txt"
        self.keys = []
        self.current_key_index = 0
        self.conversation_history = []
        self.max_history = 50
        self.model = "gemini-2.5-flash"
        self.api_base = "https://generativelanguage.googleapis.com/v1"
        
        self.cargar_keys()
        self.configurar_readline()
        self.bienvenida()
        
    def configurar_readline(self):
        histfile = Path.home() / ".xonichat_history"
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        import atexit
        atexit.register(readline.write_history_file, histfile)
        
    def cargar_keys(self):
        try:
            with open(self.keys_file, 'r') as f:
                for linea in f:
                    key = linea.strip()
                    if key and not key.startswith('#'):
                        self.keys.append(key)
        except FileNotFoundError:
            print(f"\n[ERROR] No se encuentra {self.keys_file}")
            print("[INFO] Consigue tu API key en: https://aistudio.google.com/app/apikey")
            sys.exit(1)
            
        if not self.keys:
            print("[ERROR] No hay keys validas en keys.txt")
            sys.exit(1)
            
    def bienvenida(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 60)
        print("                     XONICHAT")
        print("=" * 60)
        print(" BY: XONIDU - Darian Alberto Camacho Salas")
        print("=" * 60)
        print(f" Keys: {len(self.keys)} | Modelo: {self.model}")
        print("=" * 60)
        print("")
        
    def get_current_key(self):
        return self.keys[self.current_key_index]
        
    def cambiar_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        print(f"\n[KEY] Cambiando a key {self.current_key_index + 1}/{len(self.keys)}")
        
    def hacer_peticion(self, mensaje):
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
            "parts": [{"text": mensaje}]
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
                respuesta_json = response.json()
                if 'candidates' in respuesta_json and len(respuesta_json['candidates']) > 0:
                    respuesta = respuesta_json['candidates'][0]['content']['parts'][0]['text']
                    self.conversation_history.append({"role": "user", "content": mensaje})
                    self.conversation_history.append({"role": "assistant", "content": respuesta})
                    return respuesta
                else:
                    return "[WARNING] Respuesta vacia"
                
            elif response.status_code == 429:
                print(f"\n[WARNING] Key {self.current_key_index + 1} sin cuota")
                self.cambiar_key()
                return None
                
            elif response.status_code in [403, 404]:
                print(f"\n[ERROR] Error con key {self.current_key_index + 1}")
                if len(self.keys) > 1:
                    self.cambiar_key()
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
            
    def procesar_comando(self, cmd):
        if cmd == "/salir":
            print("\nBY: XONIDU - Darian Alberto Camacho Salas")
            print("Hasta luego!")
            sys.exit(0)
        return False
        
    def run(self):
        while True:
            try:
                prompt = f"[G{self.current_key_index+1}/{len(self.keys)}] >>> "
                mensaje = input(prompt).strip()
                
                if not mensaje:
                    continue
                    
                if mensaje == "/salir":
                    self.procesar_comando(mensaje)
                    continue
                    
                print("[...] Consultando Gemini...")
                
                respuesta = None
                intentos = 0
                max_intentos = len(self.keys) * 2
                
                while respuesta is None and intentos < max_intentos:
                    respuesta = self.hacer_peticion(mensaje)
                    if respuesta is None:
                        intentos += 1
                        time.sleep(1)
                
                if respuesta:
                    print(f"\n[G{self.current_key_index+1}]: {respuesta}\n")
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
        
    if not os.path.exists("keys.txt"):
        with open("keys.txt", "w") as f:
            f.write("# Tus API keys de Gemini (una por linea)\n")
            f.write("# Consiguelas en: https://aistudio.google.com/app/apikey\n")
        print("\n[INFO] Creado archivo keys.txt")
        print("       Pon tus API keys ahi y ejecuta de nuevo")
        print("       https://aistudio.google.com/app/apikey\n")
        sys.exit(0)
    
    app = XONICHAT()
    app.run()

if __name__ == "__main__":
    main()
