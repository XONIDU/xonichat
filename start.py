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
    """Obtiene el directorio donde está guardado este script (start.py)"""
    return os.path.dirname(os.path.abspath(__file__))

def get_fixed_xonichat_dir():
    """Devuelve la ruta fija /home/usuario/xonichat/"""
    usuario = os.path.expanduser("~")
    nombre_usuario = os.path.basename(usuario)
    return os.path.join('/home', nombre_usuario, 'xonichat')

def get_xonichat_path():
    """
    Detecta la ruta de xonichat.py:
    1. Primero busca en el mismo directorio que start.py
    2. Si no, usa la ruta fija /home/usuario/xonichat/
    """
    script_dir = get_script_dir()
    ruta_local = os.path.join(script_dir, 'xonichat.py')
    
    if os.path.exists(ruta_local):
        return ruta_local, 'local'
    
    ruta_fija = os.path.join(get_fixed_xonichat_dir(), 'xonichat.py')
    if os.path.exists(ruta_fija):
        return ruta_fija, 'fija'
    
    # Si no existe en ningún lado, devolvemos la local como predeterminada
    return ruta_local, 'ninguna'

def get_xonichat_dir():
    """Devuelve el directorio donde está xonichat.py"""
    ruta, _ = get_xonichat_path()
    return os.path.dirname(ruta)

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    ruta_xonichat, origen = get_xonichat_path()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    origen_texto = {
        'local': 'MISMO DIRECTORIO',
        'fija': '/HOME/USUARIO/XONICHAT',
        'ninguna': 'NO ENCONTRADO'
    }.get(origen, 'DESCONOCIDO')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                    XONICHAT 2026 v4.2.0                    ║
║              Cliente Gemini para Terminal                   ║
║                   Optimizado para 1GB RAM                   ║
║                                                            ║
║               Sistema detectado: {sistema_texto:<27} ║
║               Origen xonichat.py: {origen_texto:<27} ║
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

# ============================================================================
# Instalación de dependencias Python (requests)
# ============================================================================
def check_requests():
    try:
        __import__('requests')
        return True
    except ImportError:
        return False

def install_requests():
    """Instala la biblioteca requests usando pip con los flags adecuados"""
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
        # Intentar sin flags
        try:
            cmd = get_pip_command() + ['install', 'requests']
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}requests instalado correctamente.{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}Error instalando requests: {e}{Colors.END}")
            return False

# ============================================================================
# Verificación de keys.txt
# ============================================================================
def verificar_keys_txt():
    """Verifica si existe el archivo keys.txt en el directorio de xonichat"""
    xonichat_dir = get_xonichat_dir()
    keys_path = os.path.join(xonichat_dir, 'keys.txt')
    
    if not os.path.exists(keys_path):
        print(f"\n{Colors.YELLOW}⚠️ No se encuentra el archivo keys.txt{Colors.END}")
        
        # Crear archivo de ejemplo
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

# ============================================================================
# Verificación de xonichat.py y ejecución
# ============================================================================
def check_xonichat():
    ruta, origen = get_xonichat_path()
    existe = os.path.exists(ruta)
    if not existe:
        print(f"{Colors.RED}❌ No se encuentra xonichat.py{Colors.END}")
        print(f"   Buscado en: {ruta}")
    return existe

def mostrar_ayuda():
    """Muestra ayuda de uso"""
    ayuda = f"""
{Colors.BOLD}USO DE XONICHAT:{Colors.END}

  python start.py

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
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    print_banner()
    
    # Verificar argumentos de ayuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        if get_system() != 'windows':
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    sistema = get_system()
    distro = get_linux_distro()
    script_dir = get_script_dir()
    ruta_xonichat, origen = get_xonichat_path()
    xonichat_dir = get_xonichat_dir()
    
    print(f"{Colors.BOLD}Sistema operativo:{Colors.END} {sistema}")
    if distro:
        print(f"{Colors.BOLD}Distribución:{Colors.END} {distro}")
    print(f"{Colors.BOLD}Directorio de start.py:{Colors.END} {script_dir}")
    print(f"{Colors.BOLD}Origen de xonichat.py:{Colors.END} {origen}")
    print(f"{Colors.BOLD}Ruta de xonichat.py:{Colors.END} {ruta_xonichat}")
    
    # Verificar que el directorio de xonichat existe, si no, crearlo (solo para ruta fija)
    if origen == 'ninguna' and not os.path.exists(xonichat_dir):
        print(f"\n{Colors.YELLOW}⚠️ El directorio {xonichat_dir} no existe. Creándolo...{Colors.END}")
        os.makedirs(xonichat_dir, exist_ok=True)
        print(f"{Colors.GREEN}✓ Directorio creado: {xonichat_dir}{Colors.END}")
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}❌ Python no está instalado o no está en el PATH.{Colors.END}")
        sys.exit(1)
    
    # Mostrar versión de Python
    ver_py = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {ver_py}")
    
    # Verificar pip e instalarlo si falta
    if not check_pip():
        print(f"\n{Colors.YELLOW}⚠️ Pip no encontrado. Instalando...{Colors.END}")
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip. Instálalo manualmente.{Colors.END}")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip. Ejecuta como administrador.{Colors.END}")
                sys.exit(1)
        else:
            print(f"{Colors.YELLOW}Instala pip manualmente con: python -m ensurepip --upgrade{Colors.END}")
            sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ Pip disponible{Colors.END}")
    
    # Verificar e instalar requests
    if not check_requests():
        print(f"\n{Colors.YELLOW}⚠️ requests no encontrado. Instalando...{Colors.END}")
        if not install_requests():
            print(f"{Colors.RED}Fallo crítico: no se pudo instalar requests. Abortando.{Colors.END}")
            sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ requests disponible{Colors.END}")
    
    # Verificar que existe xonichat.py
    if not check_xonichat():
        print(f"\n{Colors.RED}❌ Error crítico: No se encuentra xonichat.py{Colors.END}")
        if origen == 'ninguna':
            print(f"   Puedes copiar xonichat.py a:")
            print(f"     - {script_dir} (donde está start.py)")
            print(f"     - O a {get_fixed_xonichat_dir()}")
        sys.exit(1)
    
    # Verificar/crear archivo keys.txt
    verificar_keys_txt()
    
    # Cambiar al directorio de xonichat.py
    os.chdir(xonichat_dir)
    print(f"{Colors.GREEN}✓ Cambiando al directorio: {xonichat_dir}{Colors.END}")
    
    # Ejecutar xonichat.py
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
    if sistema != 'windows':
        input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
