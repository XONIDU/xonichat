#!/usr/bin/env python3
"""
XoniChat - Cliente Google Gemini para terminal
Version con deteccion automatica de modelos
"""

import os
import sys
import time
import readline
import requests
import json
from pathlib import Path

class XoniChat:
    def __init__(self):
        self.keys_file = "keys.txt"
        self.keys = []
        self.current_key_index = 0
        self.conversation_history = []
        self.max_history = 10
        self.model = None
        self.api_base = "https://generativelanguage.googleapis.com/v1"
        
        self.cargar_keys()
        self.verificar_modelos()
        self.configurar_readline()
        
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
            print(f"Error: No se encuentra {self.keys_file}")
            print("Crea el archivo con tus API keys de Gemini (una por linea)")
            sys.exit(1)
            
        if not self.keys:
            print("Error: No hay keys validas en keys.txt")
            sys.exit(1)
            
    def verificar_modelos(self):
        """Verifica que los modelos esten disponibles"""
        key = self.keys[0]
        try:
            response = requests.get(f"{self.api_base}/models?key={key}")
            if response.status_code == 200:
                modelos = response.json().get('models', [])
                nombres = [m['name'] for m in modelos if 'generateContent' in m.get('supportedGenerationMethods', [])]
                
                if nombres:
                    # Buscar el mejor modelo disponible
                    preferidos = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                    for pref in preferidos:
                        for nombre in nombres:
                            if pref in nombre:
                                self.model = nombre.split('/')[-1]
                                break
                        if self.model:
                            break
                    
                    if not self.model and nombres:
                        self.model = nombres[0].split('/')[-1]
                        
                    print(f"[OK] {len(self.keys)} keys cargadas")
                    print(f"[OK] Modelo encontrado: {self.model}")
                else:
                    print("[error] No hay modelos disponibles para generateContent")
                    sys.exit(1)
            else:
                print(f"[error] No se pudo verificar modelos: {response.status_code}")
                print("Usando modelo por defecto: gemini-1.5-flash")
                self.model = "gemini-1.5-flash"
        except:
            print("[warning] Usando modelo por defecto: gemini-1.5-flash")
            self.model = "gemini-1.5-flash"
        
    def get_current_key(self):
        return self.keys[self.current_key_index]
        
    def cambiar_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        print(f"[cambiando] a key {self.current_key_index + 1}/{len(self.keys)}")
        
    def hacer_peticion(self, mensaje):
        key = self.get_current_key()
        url = f"{self.api_base}/models/{self.model}:generateContent?key={key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Construir historial
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
                "maxOutputTokens": 500,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                respuesta_json = response.json()
                if 'candidates' in respuesta_json and len(respuesta_json['candidates']) > 0:
                    respuesta = respuesta_json['candidates'][0]['content']['parts'][0]['text']
                    self.conversation_history.append({"role": "user", "content": mensaje})
                    self.conversation_history.append({"role": "assistant", "content": respuesta})
                    return respuesta
                else:
                    return "[error] Respuesta vacia"
                
            elif response.status_code == 429:
                print(f"[warning] Key {self.current_key_index + 1} sin cuota")
                self.cambiar_key()
                return None
                
            elif response.status_code == 403:
                print(f"[error] Key {self.current_key_index + 1} invalida")
                self.cambiar_key()
                return None
                
            elif response.status_code == 404:
                print(f"[error] Modelo {self.model} no encontrado")
                # Intentar con gemini-pro como fallback
                self.model = "gemini-pro"
                return None
                
            else:
                print(f"[error] {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("[timeout] La peticion tardo demasiado")
            return None
        except Exception as e:
            print(f"[error] {e}")
            return None
            
    def mostrar_ayuda(self):
        ayuda = """
XONICHAT - Gemini Edition
==========================
Comandos disponibles:
/help      - Muestra esta ayuda
/keys      - Muestra keys disponibles
/key N     - Cambiar a key numero N
/clear     - Limpiar pantalla
/reset     - Reiniciar conversacion
/hist      - Ver historial
/model     - Ver modelo actual
/salir     - Salir

Modelo actual: {0}
        """.format(self.model)
        print(ayuda)
        
    def procesar_comando(self, cmd):
        if cmd == "/help":
            self.mostrar_ayuda()
            return True
        elif cmd == "/keys":
            print(f"\nKeys disponibles: {len(self.keys)}")
            for i, key in enumerate(self.keys):
                mascara = key[:6] + "..." + key[-4:] if len(key) > 12 else key
                flecha = "-> " if i == self.current_key_index else "   "
                print(f"{flecha}[{i+1}] {mascara}")
            return True
        elif cmd.startswith("/key "):
            try:
                num = int(cmd.split()[1]) - 1
                if 0 <= num < len(self.keys):
                    self.current_key_index = num
                    print(f"[OK] Cambiado a key {num + 1}")
                else:
                    print(f"Error: Numero invalido (1-{len(self.keys)})")
            except:
                print("Usa: /key <numero>")
            return True
        elif cmd == "/clear":
            os.system('clear' if os.name == 'posix' else 'cls')
            return True
        elif cmd == "/reset":
            self.conversation_history = []
            print("[OK] Conversacion reiniciada")
            return True
        elif cmd == "/hist":
            if self.conversation_history:
                print("\nHistorial:")
                for i, msg in enumerate(self.conversation_history[-6:]):
                    rol = "U:" if msg['role'] == 'user' else "G:"
                    preview = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
                    print(f"{rol} {preview}")
            else:
                print("No hay historial")
            return True
        elif cmd == "/model":
            print(f"Modelo actual: {self.model}")
            return True
        elif cmd in ["/salir", "/exit", "/quit"]:
            print("XoniChat - Hasta luego")
            sys.exit(0)
        return False
        
    def run(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 50)
        print(" XONICHAT - Gemini Edition")
        print("=" * 50)
        print(f"Keys: {len(self.keys)} | Modelo: {self.model}")
        print("Escribe /help para comandos")
        print("")
        
        while True:
            try:
                prompt = f"[G{self.current_key_index+1}/{len(self.keys)}] >>> "
                mensaje = input(prompt).strip()
                
                if not mensaje:
                    continue
                    
                if mensaje.startswith('/'):
                    self.procesar_comando(mensaje)
                    continue
                    
                print("[...] consultando Gemini...")
                
                respuesta = None
                intentos = 0
                max_intentos = len(self.keys) * 3
                
                while respuesta is None and intentos < max_intentos:
                    respuesta = self.hacer_peticion(mensaje)
                    if respuesta is None:
                        intentos += 1
                        time.sleep(1)
                
                if respuesta:
                    print(f"\n[G{self.current_key_index+1}]: {respuesta}\n")
                else:
                    print("Error: No se pudo obtener respuesta")
                    
            except KeyboardInterrupt:
                print("\nXoniChat - Hasta luego")
                break
            except EOFError:
                print("\nXoniChat - Hasta luego")
                break

def main():
    try:
        import requests
    except ImportError:
        print("Instalando requests...")
        os.system("pip3 install requests --break-system-packages")
        import requests
        
    if not os.path.exists("keys.txt"):
        with open("keys.txt", "w") as f:
            f.write("# Coloca tus API keys de Google Gemini aqui (una por linea)\n")
            f.write("# Consigue tus keys gratis en: https://aistudio.google.com/app/apikey\n")
        print("[OK] Creado archivo keys.txt")
        print("    Pon tus keys ahi y ejecuta nuevamente")
        sys.exit(0)
    
    app = XoniChat()
    app.run()

if __name__ == "__main__":
    main()
