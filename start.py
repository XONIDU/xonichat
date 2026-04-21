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

def get_keys_path():
    """Detecta la ruta de keys.txt"""
    script_dir = get_script_dir()
    
    rutas = [
        os.path.join(script_dir, 'keys.txt'),
        '/usr/share/xonichat/keys.txt',
        os.path.join(os.path.expanduser("~"), 'xonichat', 'keys.txt'),
        os.path.join(os.getcwd(), 'keys.txt')
    ]
    
    for r in rutas:
        if os.path.exists(r):
            return r
    
    # Si no existe, devolver la ruta local
    return rutas[0]

def fix_permissions(file_path):
    """Arregla permisos del archivo para que sea legible por el usuario actual"""
    try:
        # Cambiar propietario al usuario actual
        uid = os.getuid()
        gid = os.getgid()
        os.chown(file_path, uid, gid)
        # Permisos: lectura/escritura para propietario
        os.chmod(file_path, 0o600)
        return True
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️ No se pudieron arreglar permisos: {e}{Colors.END}")
        return False

def manage_keys():
    """Gestión interactiva de API keys"""
    keys_path = get_keys_path()
    keys_dir = os.path.dirname(keys_path)
    
    # Crear directorio si no existe
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir, exist_ok=True)
    
    # Si el archivo no existe, crearlo
    if not os.path.exists(keys_path):
        with open(keys_path, 'w') as f:
            f.write("# Tus API keys de Gemini (una por linea)\n")
            f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n\n")
        fix_permissions(keys_path)
    
    # Leer keys existentes
    with open(keys_path, 'r') as f:
        lines = f.readlines()
    
    keys = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== GESTOR DE API KEYS ==={Colors.END}")
    print(f"📁 Ubicación: {keys_path}")
    print(f"🔑 Keys activas: {len(keys)}")
    print(f"🔗 Obtener keys: {Colors.GREEN}https://aistudio.google.com/app/apikey{Colors.END}")
    
    # Mostrar keys existentes
    if keys:
        print(f"\n{Colors.BOLD}Keys actuales:{Colors.END}")
        for i, key in enumerate(keys, 1):
            # Mostrar solo últimos 8 caracteres por seguridad
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
            fix_permissions(keys_path)
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
                    key_eliminada = keys.pop(eliminar - 1)
                    # Reescribir archivo sin la key eliminada
                    with open(keys_path, 'w') as f:
                        f.write("# Tus API keys de Gemini (una por linea)\n")
                        f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n\n")
                        for key in keys:
                            f.write(f"{key}\n")
                    fix_permissions(keys_path)
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
# Verificación de permisos
# ============================================================================
def check_permissions(file_path):
    """Verifica si el archivo es legible por el usuario actual"""
    if not os.path.exists(file_path):
        return True
    try:
        with open(file_path, 'r'):
            pass
        return True
    except PermissionError:
        return False

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

# ============================================================================
# Verificación de xonichat.py y ejecución
# ============================================================================
def get_xonichat_path():
    """Detecta la ruta de xonichat.py en múltiples ubicaciones"""
    script_dir = get_script_dir()
    
    rutas = [
        os.path.join(script_dir, 'xonichat.py'),
        '/usr/share/xonichat/xonichat.py',
        os.path.join(os.path.expanduser("~"), 'xonichat', 'xonichat.py'),
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
║                    XONICHAT 2026 v4.2.1                    ║
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
  ✅ Gestor interactivo de keys - Agrega o elimina keys facilmente

{Colors.BOLD}COMANDOS:{Colors.END}

  /salir     - Terminar la conversacion
  Ctrl+C     - Salir del programa

{Colors.BOLD}OBTENER API KEYS:{Colors.END}

  https://aistudio.google.com/app/apikey
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
        sys.exit(1)
    
    xonichat_dir = os.path.dirname(ruta_xonichat)
    print(f"{Colors.GREEN}✓ xonichat.py encontrado en: {xonichat_dir}{Colors.END}")
    
    # Gestionar keys (preguntar al usuario)
    keys_path = manage_keys()
    
    # Verificar permisos del archivo keys.txt
    if os.path.exists(keys_path) and not check_permissions(keys_path):
        print(f"{Colors.YELLOW}⚠️ Problemas de permisos en {keys_path}{Colors.END}")
        fix_permissions(keys_path)
    
    # Cambiar al directorio y ejecutar
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
