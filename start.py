#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICHAT 2026 - Lanzador Universal con Gestor de Keys
Cliente Gemini desde terminal para equipos de bajos recursos
Desarrollador: Darian Alberto Camacho Salas
Organización: XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import time
from pathlib import Path

# ============================================================================
# Colores para terminal
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Detección del sistema
# ============================================================================
def get_system():
    return platform.system().lower()

def get_linux_distro():
    if get_system() != 'linux':
        return None
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content or 'mint' in content or 'antix' in content:
                    return 'debian-based'
                elif 'arch' in content or 'manjaro' in content:
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content or 'rhel' in content:
                    return 'centos'
                elif 'opensuse' in content:
                    return 'opensuse'
        if shutil.which('apt'):
            return 'debian-based'
        elif shutil.which('pacman'):
            return 'arch-based'
        elif shutil.which('dnf'):
            return 'fedora'
        elif shutil.which('yum'):
            return 'centos'
        elif shutil.which('zypper'):
            return 'opensuse'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def get_pip_command():
    return [sys.executable, '-m', 'pip']

def get_install_flags():
    flags = []
    sistema = get_system()
    distro = get_linux_distro()
    if sistema == 'linux':
        if distro in ['arch-based', 'fedora']:
            flags.append('--break-system-packages')
        else:
            flags.append('--user')
    elif sistema == 'darwin':
        flags.append('--user')
    return flags

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_xonichat_path():
    """Detecta la ruta de xonichat.py en múltiples ubicaciones"""
    script_dir = get_script_dir()
    rutas = [
        os.path.join(script_dir, 'xonichat.py'),
        '/usr/share/xonichat/xonichat.py',
        os.path.join(os.path.expanduser("~"), '.xonichat', 'xonichat.py'),
        os.path.join(os.getcwd(), 'xonichat.py')
    ]
    for r in rutas:
        if os.path.exists(r):
            return r
    return None

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                    XONICHAT 2026 v4.2.7                    ║
║              Cliente Gemini para Terminal                   ║
║                   Optimizado para 1GB RAM                   ║
║                                                            ║
║               Sistema detectado: {sistema_texto:<27} ║
║                                                            ║
║               Desarrollado por: Darian Alberto             ║
║                      Camacho Salas                         ║
║                      Organización: XONIDU                  ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}USO DE XONICHAT:{Colors.END}

  xonichat

{Colors.BOLD}CARACTERISTICAS:{Colors.END}

  ✅ Interfaz 100% terminal
  ✅ Multiples API keys con rotacion automatica
  ✅ Gestor interactivo de keys
  ✅ Sin necesidad de sudo

{Colors.BOLD}COMANDOS:{Colors.END}

  /salir     - Terminar la conversacion
  Ctrl+C     - Salir del programa

{Colors.BOLD}OBTENER API KEYS:{Colors.END}

  https://aistudio.google.com/app/apikey
    """
    print(ayuda)

# ============================================================================
# Clase principal XONICHAT
# ============================================================================
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
        
        # Opción 2: Mismo directorio que start.py
        script_dir = get_script_dir()
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
        try:
            import readline
            histfile = Path.home() / ".xonichat_history"
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass
            import atexit
            atexit.register(readline.write_history_file, histfile)
        except ImportError:
            pass  # Windows no tiene readline
    
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

# ============================================================================
# Verificación de dependencias
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def install_pip_linux():
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    if distro == 'debian-based':
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=False)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'arch-based':
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], check=True)
            return True
        except:
            return False
    return False

def install_pip_windows():
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        return False

def check_requests():
    try:
        __import__('requests')
        return True
    except ImportError:
        return False

def install_requests():
    print(f"{Colors.YELLOW}Instalando requests...{Colors.END}")
    if not check_pip():
        return False
    flags = get_install_flags()
    try:
        cmd = get_pip_command() + ['install', 'requests'] + flags
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"{Colors.GREEN}requests instalado correctamente.{Colors.END}")
        return True
    except:
        try:
            cmd = get_pip_command() + ['install', 'requests']
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}requests instalado correctamente.{Colors.END}")
            return True
        except:
            return False

def manage_keys():
    """Gestión interactiva de API keys"""
    keys_path = XONICHAT().get_keys_path()
    keys_dir = os.path.dirname(keys_path)
    
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir, exist_ok=True)
    
    if not os.path.exists(keys_path):
        with open(keys_path, 'w') as f:
            f.write("# Tus API keys de Gemini (una por linea)\n")
            f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n\n")
    
    with open(keys_path, 'r') as f:
        lines = f.readlines()
    
    keys = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== GESTOR DE API KEYS ==={Colors.END}")
    print(f"📁 Ubicación: {keys_path}")
    print(f"🔑 Keys activas: {len(keys)}")
    print(f"🔗 Obtener keys: {Colors.GREEN}https://aistudio.google.com/app/apikey{Colors.END}")
    
    if keys:
        print(f"\n{Colors.BOLD}Keys actuales:{Colors.END}")
        for i, key in enumerate(keys, 1):
            masked = key[:15] + "..." + key[-8:] if len(key) > 30 else key
            print(f"  {i}. {masked}")
    
    print(f"\n{Colors.BOLD}Opciones:{Colors.END}")
    print("  1. Agregar nueva API key")
    print("  2. Eliminar una API key")
    print("  3. Salir (continuar con las keys actuales)")
    
    opcion = input(f"\n{Colors.YELLOW}Elige una opción (1-3): {Colors.END}").strip()
    
    if opcion == '1':
        nueva_key = input(f"{Colors.CYAN}Ingresa la nueva API key: {Colors.END}").strip()
        if nueva_key and nueva_key.startswith('AIza'):
            with open(keys_path, 'a') as f:
                f.write(f"{nueva_key}\n")
            print(f"{Colors.GREEN}✅ Key agregada correctamente{Colors.END}")
            time.sleep(1)
        else:
            print(f"{Colors.RED}❌ Key inválida. Debe comenzar con 'AIza'{Colors.END}")
            time.sleep(1)
    
    elif opcion == '2':
        if not keys:
            print(f"{Colors.YELLOW}⚠️ No hay keys para eliminar{Colors.END}")
            time.sleep(1)
        else:
            print(f"\n{Colors.BOLD}Selecciona la key a eliminar:{Colors.END}")
            for i, key in enumerate(keys, 1):
                masked = key[:15] + "..." + key[-8:] if len(key) > 30 else key
                print(f"  {i}. {masked}")
            
            try:
                eliminar = int(input(f"{Colors.YELLOW}Número de key a eliminar (0 = cancelar): {Colors.END}"))
                if 1 <= eliminar <= len(keys):
                    keys.pop(eliminar - 1)
                    with open(keys_path, 'w') as f:
                        f.write("# Tus API keys de Gemini (una por linea)\n")
                        f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n\n")
                        for key in keys:
                            f.write(f"{key}\n")
                    print(f"{Colors.GREEN}✅ Key eliminada correctamente{Colors.END}")
                    time.sleep(1)
                elif eliminar == 0:
                    print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ Número inválido{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Entrada inválida{Colors.END}")
    
    print(f"{Colors.GREEN}✅ Continuando con {len(keys)} key(s)...{Colors.END}")
    return keys_path

# ============================================================================
# Función principal
# ============================================================================
def main():
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    print_banner()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        if get_system() != 'windows':
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    if not check_python():
        print(f"\n{Colors.RED}❌ Python no esta instalado{Colors.END}")
        sys.exit(1)
    
    ver_py = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {ver_py}")
    
    if not check_pip():
        print(f"\n{Colors.YELLOW}⚠️ Pip no encontrado. Instalando...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip.{Colors.END}")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip.{Colors.END}")
                sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ Pip disponible{Colors.END}")
    
    if not check_requests():
        print(f"\n{Colors.YELLOW}⚠️ requests no encontrado. Instalando...{Colors.END}")
        if not install_requests():
            print(f"{Colors.RED}No se pudo instalar requests.{Colors.END}")
            sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ requests disponible{Colors.END}")
    
    ruta_xonichat = get_xonichat_path()
    if not ruta_xonichat:
        print(f"\n{Colors.RED}❌ No se encuentra xonichat.py{Colors.END}")
        sys.exit(1)
    
    xonichat_dir = os.path.dirname(ruta_xonichat)
    print(f"{Colors.GREEN}✓ xonichat.py encontrado en: {xonichat_dir}{Colors.END}")
    
    manage_keys()
    
    os.chdir(xonichat_dir)
    print(f"\n{Colors.BOLD}🚀 Iniciando XONICHAT...{Colors.END}")
    print(f"{Colors.CYAN}Para salir: escribe '/salir' o presiona Ctrl+C{Colors.END}")
    print("-"*50)
    
    try:
        python_cmd = get_python_command()
        subprocess.run(python_cmd + [ruta_xonichat])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Programa detenido por el usuario.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
    
    print(f"\n{Colors.GREEN}Gracias por usar XONICHAT{Colors.END}")
    if get_system() != 'windows':
        input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
