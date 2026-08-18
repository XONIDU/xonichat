#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICHAT 2026 - Cliente Gemini para Terminal
Optimizado para equipos de bajos recursos (Linux, Windows, macOS)
Desarrollador: Darian Alberto Camacho Salas
Organización: XONIDU
"""

import os
import sys
import time
import platform
from pathlib import Path

# Intentar importar readline (solo Linux/macOS)
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

# Intentar importar requests
try:
    import requests
except ImportError:
    print("[INFO] Instalando requests...")
    os.system("pip install requests --quiet" if platform.system() == 'Windows' else "pip3 install requests --break-system-packages --quiet")
    import requests


class Colors:
    """Colores para terminal - soporte para Windows y Linux"""
    GREEN = '\033[92m' if platform.system() != 'Windows' else ''
    YELLOW = '\033[93m' if platform.system() != 'Windows' else ''
    RED = '\033[91m' if platform.system() != 'Windows' else ''
    PURPLE = '\033[95m' if platform.system() != 'Windows' else ''
    CYAN = '\033[96m' if platform.system() != 'Windows' else ''
    END = '\033[0m' if platform.system() != 'Windows' else ''
    BOLD = '\033[1m' if platform.system() != 'Windows' else ''
    
    @staticmethod
    def supports_color():
        """Verifica si la terminal soporta colores"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True


# Desactivar colores si no hay soporte
if platform.system() == 'Windows' and not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')


class XONICHAT:
    def __init__(self):
        self.user_home = os.path.expanduser("~")
        self.is_windows = platform.system() == 'Windows'
        self.is_linux = platform.system() == 'Linux'
        self.is_macos = platform.system() == 'Darwin'
        
        self.keys_file = self.get_keys_path()
        self.keys = []
        self.current_key_index = 0
        self.conversation_history = []
        self.max_history = 50
        self.model = "gemini-2.5-flash"
        self.api_base = "https://generativelanguage.googleapis.com/v1beta"
        
        # Crear directorio de keys si no existe
        self.ensure_keys_dir()
        
        self.load_keys()
        self.setup_readline()
        self.welcome()
    
    def get_keys_path(self):
        """Busca keys.txt priorizando ~/.xonichat/ (sin sudo)"""
        
        # Opción 1: Directorio en HOME (recomendado, sin sudo)
        home_keys = os.path.join(self.user_home, '.xonichat', 'keys.txt')
        if os.path.exists(home_keys):
            return home_keys
        
        # Opción 2: Mismo directorio que el script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_keys = os.path.join(script_dir, 'keys.txt')
        if os.path.exists(local_keys):
            return local_keys
        
        # Opción 3: /usr/share/xonichat/ (legacy, solo Linux)
        if self.is_linux:
            system_keys = '/usr/share/xonichat/keys.txt'
            if os.path.exists(system_keys):
                return system_keys
        
        # Si no existe, devolver ruta en HOME
        return home_keys
    
    def ensure_keys_dir(self):
        """Asegura que el directorio de keys existe"""
        keys_dir = os.path.dirname(self.keys_file)
        if not os.path.exists(keys_dir):
            try:
                os.makedirs(keys_dir, exist_ok=True)
                return True
            except Exception as e:
                print(f"[WARNING] No se pudo crear {keys_dir}: {e}")
                return False
        return True
    
    def setup_readline(self):
        """Configura readline si está disponible"""
        if not READLINE_AVAILABLE:
            return
        
        try:
            histfile = Path.home() / ".xonichat_history"
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass
            import atexit
            atexit.register(readline.write_history_file, histfile)
        except Exception:
            pass
    
    def load_keys(self):
        """Carga las API keys desde el archivo"""
        # Si el archivo no existe, crearlo con instrucciones
        if not os.path.exists(self.keys_file):
            self.create_keys_template()
            print(f"\n{Colors.YELLOW}[INFO] No se encontró keys.txt{Colors.END}")
            print(f"[INFO] Se ha creado una plantilla en: {self.keys_file}")
            print(f"[INFO] Agrega tus API keys y vuelve a ejecutar")
            print(f"[INFO] Obtén tus keys en: {Colors.CYAN}https://aistudio.google.com/app/apikey{Colors.END}\n")
            sys.exit(1)
        
        # Cargar keys
        try:
            with open(self.keys_file, 'r', encoding='utf-8') as f:
                for line in f:
                    key = line.strip()
                    if key and not key.startswith('#'):
                        self.keys.append(key)
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] No se pudo leer {self.keys_file}{Colors.END}")
            print(f"[ERROR] {e}")
            sys.exit(1)
        
        # Validar keys
        if not self.keys:
            print(f"\n{Colors.YELLOW}[WARNING] No hay keys validas en keys.txt{Colors.END}")
            print(f"[INFO] Agrega tus API keys en: {self.keys_file}")
            print(f"[INFO] Obtén tus keys en: {Colors.CYAN}https://aistudio.google.com/app/apikey{Colors.END}\n")
            sys.exit(1)
        
        # Validar formato de keys
        valid_keys = []
        invalid_keys = []
        for key in self.keys:
            if key.startswith('AIzaSy') and len(key) > 20:
                valid_keys.append(key)
            else:
                invalid_keys.append(key)
        
        if invalid_keys:
            print(f"{Colors.YELLOW}[WARNING] {len(invalid_keys)} key(s) inválidas encontradas{Colors.END}")
        
        self.keys = valid_keys
        
        if not self.keys:
            print(f"\n{Colors.RED}[ERROR] No hay keys válidas{Colors.END}")
            print(f"[INFO] Las keys deben comenzar con 'AIzaSy'")
            sys.exit(1)
    
    def create_keys_template(self):
        """Crea un archivo keys.txt con instrucciones"""
        keys_dir = os.path.dirname(self.keys_file)
        if not os.path.exists(keys_dir):
            os.makedirs(keys_dir, exist_ok=True)
        
        with open(self.keys_file, 'w', encoding='utf-8') as f:
            f.write("# ============================================================\n")
            f.write("# XONICHAT - API Keys de Gemini\n")
            f.write("# ============================================================\n")
            f.write("#\n")
            f.write("# INSTRUCCIONES:\n")
            f.write("# 1. Ve a: https://aistudio.google.com/app/apikey\n")
            f.write("# 2. Inicia sesión con tu cuenta Google\n")
            f.write("# 3. Crea una nueva API key (comienza con AIzaSy...)\n")
            f.write("# 4. Copia la key y pégala en este archivo (una por línea)\n")
            f.write("#\n")
            f.write("# Las líneas que comienzan con # son ignoradas\n")
            f.write("# ============================================================\n\n")
            f.write("# Ejemplo (reemplaza con tus propias keys):\n")
            f.write("# AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********\n")
            f.write("# AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********\n\n")
            f.write("# === TUS API KEYS AQUÍ ===\n")
    
    def welcome(self):
        """Muestra el banner de bienvenida"""
        os.system('cls' if self.is_windows else 'clear')
        print("=" * 60)
        print("                     XONICHAT")
        print("=" * 60)
        print(" BY: XONIDU - Darian Alberto Camacho Salas")
        print("=" * 60)
        print(f" Keys: {len(self.keys)} | Model: {self.model}")
        print(f" Keys file: {self.keys_file}")
        print(f" OS: {platform.system()} {platform.release()}")
        print("=" * 60)
        print("")
    
    def get_current_key(self):
        """Obtiene la key activa actual"""
        if not self.keys:
            return None
        return self.keys[self.current_key_index]
    
    def switch_key(self):
        """Cambia a la siguiente key disponible"""
        if len(self.keys) <= 1:
            print(f"\n{Colors.RED}[ERROR] Solo hay una key disponible{Colors.END}")
            return False
        
        old_index = self.current_key_index
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        print(f"\n{Colors.YELLOW}[KEY] Cambiando de key {old_index + 1} → {self.current_key_index + 1}/{len(self.keys)}{Colors.END}")
        return True
    
    def make_request(self, message):
        """Realiza una petición a la API de Gemini"""
        if not self.keys:
            print(f"\n{Colors.RED}[ERROR] No hay keys disponibles{Colors.END}")
            return None
        
        key = self.get_current_key()
        url = f"{self.api_base}/models/{self.model}:generateContent?key={key}"
        headers = {"Content-Type": "application/json"}
        
        # Construir contenido con historial
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
                    return f"{Colors.YELLOW}[WARNING] Respuesta vacía{Colors.END}"
                
            elif response.status_code == 429:
                print(f"\n{Colors.YELLOW}[WARNING] Key {self.current_key_index + 1} sin cuota{Colors.END}")
                if self.switch_key():
                    return None
                else:
                    return f"{Colors.RED}[ERROR] Todas las keys sin cuota{Colors.END}"
                
            elif response.status_code in [403, 404]:
                print(f"\n{Colors.RED}[ERROR] Key {self.current_key_index + 1} inválida{Colors.END}")
                if len(self.keys) > 1:
                    self.switch_key()
                    return None
                else:
                    return f"{Colors.RED}[ERROR] Key inválida, no hay más keys{Colors.END}"
                
            elif response.status_code == 400:
                error_msg = response.json().get('error', {}).get('message', 'Error desconocido')
                print(f"\n{Colors.RED}[ERROR] 400 - {error_msg}{Colors.END}")
                return None
                
            else:
                print(f"\n{Colors.RED}[ERROR] {response.status_code}{Colors.END}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"\n{Colors.RED}[TIMEOUT] La petición tardó demasiado{Colors.END}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"\n{Colors.RED}[ERROR] No hay conexión a Internet{Colors.END}")
            return None
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] {e}{Colors.END}")
            return None
    
    def process_command(self, cmd):
        """Procesa comandos especiales"""
        if cmd in ["/salir", "/exit", "/quit"]:
            print(f"\n{Colors.CYAN}BY: XONIDU - Darian Alberto Camacho Salas{Colors.END}")
            print(f"{Colors.CYAN}¡Hasta luego!{Colors.END}")
            sys.exit(0)
        elif cmd == "/keys":
            print(f"\n{Colors.BOLD}Keys activas: {len(self.keys)}{Colors.END}")
            for i, key in enumerate(self.keys, 1):
                masked = key[:15] + "..." + key[-8:] if len(key) > 30 else key
                status = f"{Colors.GREEN}✓ Activa{Colors.END}" if i == self.current_key_index + 1 else "   "
                print(f"  {i}. {masked} {status}")
            return True
        elif cmd == "/help":
            self.show_help()
            return True
        return False
    
    def show_help(self):
        """Muestra la ayuda"""
        help_text = f"""
{Colors.BOLD}COMANDOS DISPONIBLES:{Colors.END}
  {Colors.CYAN}/salir{Colors.END}   - Terminar la conversación
  {Colors.CYAN}/exit{Colors.END}    - Terminar la conversación
  {Colors.CYAN}/quit{Colors.END}    - Terminar la conversación
  {Colors.CYAN}/keys{Colors.END}    - Mostrar estado de las API keys
  {Colors.CYAN}/help{Colors.END}    - Mostrar esta ayuda

{Colors.BOLD}USO:{Colors.END}
  Escribe tu mensaje y presiona Enter para enviarlo a Gemini
  El programa muestra qué key está activa con [G1/2]

{Colors.BOLD}CONFIGURACIÓN:{Colors.END}
  Archivo de keys: {self.keys_file}
  Modelo: {self.model}
"""
        print(help_text)
    
    def run(self):
        """Bucle principal del programa"""
        while True:
            try:
                if not self.keys:
                    print(f"\n{Colors.RED}[ERROR] No hay keys disponibles{Colors.END}")
                    break
                
                prompt = f"{Colors.CYAN}[G{self.current_key_index+1}/{len(self.keys)}]{Colors.END} >>> "
                message = input(prompt).strip()
                
                if not message:
                    continue
                
                if message.startswith('/'):
                    self.process_command(message)
                    continue
                
                print(f"{Colors.YELLOW}[...] Consultando Gemini...{Colors.END}")
                
                response = None
                attempts = 0
                max_attempts = len(self.keys) * 2
                
                while response is None and attempts < max_attempts:
                    response = self.make_request(message)
                    if response is None:
                        attempts += 1
                        if attempts < max_attempts:
                            print(f"{Colors.YELLOW}[...] Reintentando ({attempts}/{max_attempts})...{Colors.END}")
                            time.sleep(1)
                
                if response:
                    print(f"\n{Colors.GREEN}[G{self.current_key_index+1}]{Colors.END}: {response}\n")
                else:
                    print(f"\n{Colors.RED}[ERROR] No se pudo obtener respuesta{Colors.END}\n")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.CYAN}BY: XONIDU - Darian Alberto Camacho Salas{Colors.END}")
                print(f"{Colors.CYAN}¡Hasta luego!{Colors.END}")
                break
            except EOFError:
                print(f"\n\n{Colors.CYAN}BY: XONIDU - Darian Alberto Camacho Salas{Colors.END}")
                print(f"{Colors.CYAN}¡Hasta luego!{Colors.END}")
                break
            except Exception as e:
                print(f"\n{Colors.RED}[ERROR] {e}{Colors.END}")


def main():
    try:
        app = XONICHAT()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}BY: XONIDU - Darian Alberto Camacho Salas{Colors.END}")
        print(f"{Colors.CYAN}¡Hasta luego!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] {e}{Colors.END}")


if __name__ == "__main__":
    main()