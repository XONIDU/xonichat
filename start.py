#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICHAT 2026 - Lanzador Universal (Robusto)
Cliente Gemini desde terminal para equipos de bajos recursos
Incluye instalación automática de pip, requests y manejo de API keys
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
    """
    Detecta la ruta de xonichat.py en múltiples ubicaciones posibles
    1. Mismo directorio que start.py (instalación manual)
    2. /usr/share/xonichat/ (instalación desde AUR)
    3. /home/usuario/xonichat/ (ruta fija alternativa)
    """
    script_dir = get_script_dir()
    
    # Opción 1: Mismo directorio que start.py
    ruta_local = os.path.join(script_dir, 'xonichat.py')
    if os.path.exists(ruta_local):
        return ruta_local
    
    # Opción 2: Instalación desde AUR
    ruta_aur = '/usr/share/xonichat/xonichat.py'
    if os.path.exists(ruta_aur):
        return ruta_aur
    
    # Opción 3: Ruta fija en home del usuario
    usuario = os.path.expanduser("~")
    ruta_home = os.path.join(usuario, 'xonichat', 'xonichat.py')
    if os.path.exists(ruta_home):
        return ruta_home
    
    # Opción 4: Ruta local alternativa (./xonichat.py)
    ruta_actual = os.path.join(os.getcwd(), 'xonichat.py')
    if os.path.exists(ruta_actual):
        return ruta_actual
    
    return None

def get_xonichat_dir():
    ruta = get_xonichat_path()
    if ruta:
        return os.path.dirname(ruta)
    return None

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    ruta_xonichat = get_xonichat_path()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    estado = "✅ ENCONTRADO" if ruta_xonichat else "❌ NO ENCONTRADO"
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                    XONICHAT 2026 v4.2.0                    ║
║              Cliente Gemini para Terminal                   ║
║                   Optimizado para 1GB RAM                   ║
║                                                            ║
║               Sistema detectado: {sistema_texto:<27} ║
║               Estado xonichat.py: {estado:<27} ║
║                                                            ║
║               Desarrollado por: Darian Alberto             ║
║                      Camacho Salas                         ║
║                      Organización: XONIDU                  ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

# ============================================================================
# Verificación e instalación de pip
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
    elif distro == 'fedora':
        try:
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'centos':
        try:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'opensuse':
        try:
            subprocess.run(['sudo', 'zypper', 'install', '-y', 'python3-pip'], check=True)
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
        try:
            import urllib.request
            urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
            subprocess.run([sys.executable, 'get-pip.py'], check=True)
            os.remove('get-pip.py')
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
        print(f"{Colors.RED}No se encontró pip. Instálalo primero.{Colors.END}")
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
        except Exception as e:
            print(f"{Colors.RED}Error instalando requests: {e}{Colors.END}")
            return False

def verificar_keys_txt():
    xonichat_dir = get_xonichat_dir()
    if not xonichat_dir:
        print(f"\n{Colors.RED}❌ No se puede determinar directorio de xonichat.py{Colors.END}")
        return False
    
    keys_path = os.path.join(xonichat_dir, 'keys.txt')
    
    if not os.path.exists(keys_path):
        print(f"\n{Colors.YELLOW}⚠️ No se encuentra el archivo keys.txt{Colors.END}")
        with open(keys_path, 'w') as f:
            f.write("# Tus API keys de Gemini (una por linea)\n")
            f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n")
            f.write("\n")
            f.write("# Ejemplo:\n")
            f.write("# AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********\n")
            f.write("# AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********\n")
        print(f"{Colors.GREEN}✓ Archivo keys.txt creado en {xonichat_dir}{Colors.END}")
        print(f"\n{Colors.YELLOW}⚠️ EDITA EL ARCHIVO keys.txt Y AGREGA TUS API KEYS{Colors.END}")
        print(f"{Colors.CYAN}   Puedes obtener keys gratis en: https://aistudio.google.com/app/apikey{Colors.END}")
        if get_system() != 'windows':
            input(f"\n{Colors.YELLOW}Presiona Enter después de configurar tus keys...{Colors.END}")
        return False
    return True

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}USO DE XONICHAT:{Colors.END}

  xonichat              # Iniciar el programa
  python start.py       # Iniciar manualmente

{Colors.BOLD}DESCRIPCION:{Colors.END}

  XONICHAT es un cliente de inteligencia artificial por terminal
  que permite interactuar con el modelo Gemini de Google desde
  equipos de bajos recursos.

{Colors.BOLD}CARACTERISTICAS:{Colors.END}

  ✅ Interfaz 100%% terminal - Rapida y ligera
  ✅ Multiples API keys - Cambio automatico cuando una se agota
  ✅ Historial de conversacion - Contexto entre mensajes
  ✅ Optimizado - Funciona en ASUS Eee PC y equipos similares

{Colors.BOLD}COMANDOS:{Colors.END}

  /salir     - Terminar la conversacion
  Ctrl+C     - Salir del programa

{Colors.BOLD}CONFIGURACION:{Colors.END}

  1. Obtener API keys: https://aistudio.google.com/app/apikey
  2. Crear archivo keys.txt con tus keys (una por linea)
  
{Colors.BOLD}EJEMPLO keys.txt:{Colors.END}
  # Tus API keys de Gemini
  AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********
  AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********
    """
    print(ayuda)

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
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}❌ Python no está instalado o no está en el PATH.{Colors.END}")
        sys.exit(1)
    
    ver_py = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {ver_py}")
    
    # Verificar pip
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
    
    # Verificar requests
    if not check_requests():
        print(f"\n{Colors.YELLOW}⚠️ requests no encontrado. Instalando...{Colors.END}")
        if not install_requests():
            print(f"{Colors.RED}Fallo crítico: no se pudo instalar requests.{Colors.END}")
            sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ requests disponible{Colors.END}")
    
    # Verificar xonichat.py
    ruta_xonichat = get_xonichat_path()
    if not ruta_xonichat:
        print(f"\n{Colors.RED}❌ No se encuentra xonichat.py{Colors.END}")
        print("   Buscado en:")
        print("     - Mismo directorio que start.py")
        print("     - /usr/share/xonichat/")
        print("     - ~/xonichat/")
        print("     - Directorio actual")
        sys.exit(1)
    
    xonichat_dir = os.path.dirname(ruta_xonichat)
    print(f"{Colors.GREEN}✓ xonichat.py encontrado en: {xonichat_dir}{Colors.END}")
    
    # Verificar keys.txt
    keys_path = os.path.join(xonichat_dir, 'keys.txt')
    if not os.path.exists(keys_path):
        verificar_keys_txt()
    
    # Cambiar al directorio y ejecutar
    os.chdir(xonichat_dir)
    print(f"\n{Colors.BOLD}🚀 Iniciando XONICHAT...{Colors.END}")
    print(f"{Colors.CYAN}Para salir: escribe '/salir' o presiona Ctrl+C{Colors.END}")
    print("-"*50)
    
    try:
        python_cmd = get_python_command()
        subprocess.run(python_cmd + ['xonichat.py'])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Programa detenido por el usuario.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error ejecutando xonichat.py: {e}{Colors.END}")
    
    print(f"\n{Colors.GREEN}Gracias por usar XONICHAT 2026{Colors.END}")
    if get_system() != 'windows':
        input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
