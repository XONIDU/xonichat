#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICHAT 2026 - Lanzador Universal de Cliente Gemini para Terminal
Este script ejecuta xonichat.py y verifica dependencias
Desarrollado por: Darian Alberto Camacho Salas
#Somos XONINDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util
import time

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
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
if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribucion de Linux"""
    if get_system() != 'linux':
        return None
    
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    return 'ubuntu'
                elif 'debian' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content:
                    return 'centos'
                elif 'arch' in content:
                    return 'arch'
                elif 'manjaro' in content:
                    return 'manjaro'
                elif 'mint' in content:
                    return 'mint'
                elif 'opensuse' in content or 'suse' in content:
                    return 'opensuse'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def check_pip():
    """Verifica si pip está instalado"""
    try:
        cmd = [sys.executable, '-m', 'pip', '--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_pip_linux():
    """Instala pip en Linux según la distribución detectada"""
    distro = get_linux_distro()
    print(f"{Colors.BOLD}Instalando pip en {distro}...{Colors.END}")
    
    if distro in ['ubuntu', 'debian', 'mint', 'antix']:
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=False)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            print(f"{Colors.GREEN}Pip instalado correctamente{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}Error instalando pip con apt{Colors.END}")
            return False
    
    elif distro in ['arch', 'manjaro']:
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], check=True)
            print(f"{Colors.GREEN}Pip instalado correctamente{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}Error instalando pip con pacman{Colors.END}")
            return False
    
    elif distro in ['fedora']:
        try:
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'python3-pip'], check=True)
            print(f"{Colors.GREEN}Pip instalado correctamente{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}Error instalando pip con dnf{Colors.END}")
            return False
    
    elif distro in ['centos']:
        try:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'python3-pip'], check=True)
            print(f"{Colors.GREEN}Pip instalado correctamente{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}Error instalando pip con yum{Colors.END}")
            return False
    
    elif distro in ['opensuse']:
        try:
            subprocess.run(['sudo', 'zypper', 'install', '-y', 'python3-pip'], check=True)
            print(f"{Colors.GREEN}Pip instalado correctamente{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}Error instalando pip con zypper{Colors.END}")
            return False
    
    else:
        print(f"{Colors.YELLOW}Distribución no reconocida. Instala pip manualmente.{Colors.END}")
        print("Consulta: https://pip.pypa.io/en/stable/installation/")
        return False

def print_banner():
    """Muestra el banner de XONICHAT"""
    sistema = get_system()
    distro = get_linux_distro()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.BLUE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                    XONICHAT 2026 v4.2.0                    
              Cliente Gemini para Terminal            
              Optimizado para equipos de bajos recursos       
              ASUS Eee PC, antiX Linux, Termux                
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
              #Somos XONINDU
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica Python instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_command(comando):
    """Verifica si un comando existe"""
    return shutil.which(comando) is not None

def check_python_module(module_name):
    """Verifica si un modulo de Python esta instalado"""
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    """Verifica las dependencias de Python necesarias"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    dependencias = [
        ('requests', 'requests', 'Peticiones HTTP', 'requests'),
    ]
    
    faltantes = []
    
    for modulo, paquete, desc, import_name in dependencias:
        if check_python_module(import_name):
            print(f"{Colors.GREEN}  - {modulo}: OK{Colors.END}")
        else:
            print(f"{Colors.YELLOW}  - {modulo}: FALTANTE{Colors.END}")
            faltantes.append(paquete)
    
    return faltantes

def install_dependencies(faltantes):
    """Instala las dependencias faltantes"""
    if not faltantes:
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    sistema = get_system()
    distro = get_linux_distro()
    
    # Instalar paquetes Python
    if faltantes:
        print(f"Paquetes Python a instalar: {', '.join(faltantes)}")
        
        # Construir comando de instalacion
        cmd = [sys.executable, '-m', 'pip', 'install']
        
        # Agregar opciones segun sistema
        if sistema == 'linux':
            if distro in ['arch', 'manjaro', 'fedora']:
                cmd.append('--break-system-packages')
                print(f"{Colors.YELLOW}Usando --break-system-packages para {distro}{Colors.END}")
            else:
                cmd.append('--user')
        elif sistema == 'darwin':
            cmd.append('--user')
        
        cmd.extend(faltantes)
        
        # Intentar instalacion
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias instaladas correctamente{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            print(f"\n{Colors.YELLOW}Intentando metodo alternativo...{Colors.END}")
            
            # Segundo intento: solo --user
            try:
                cmd2 = [sys.executable, '-m', 'pip', 'install', '--user'] + faltantes
                subprocess.run(cmd2, check=True)
                print(f"{Colors.GREEN}Instaladas con --user{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}Fallo la instalacion{Colors.END}")
                print(f"\nInstala manualmente:")
                print(f"  pip install {' '.join(faltantes)}")
                return False
    
    return True

def verificar_archivo_keys():
    """Verifica si existe el archivo keys.txt"""
    if not os.path.exists('keys.txt'):
        print(f"\n{Colors.YELLOW}No se encuentra el archivo keys.txt{Colors.END}")
        
        # Crear archivo de ejemplo
        with open('keys.txt', 'w') as f:
            f.write("# Tus API keys de Gemini (una por linea)\n")
            f.write("# Obtenlas en: https://aistudio.google.com/app/apikey\n")
            f.write("# AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********\n")
            f.write("# AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********\n")
        
        print(f"{Colors.GREEN}Archivo keys.txt creado con plantilla de ejemplo{Colors.END}")
        print(f"\n{Colors.YELLOW}EDITA EL ARCHIVO keys.txt Y AGREGA TUS API KEYS{Colors.END}")
        print("Presiona Enter cuando hayas configurado tus keys...")
        input()
        return False
    return True

def verificar_importaciones():
    """Verifica que todas las importaciones necesarias funcionen"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    modulos = [
        ('requests', 'requests'),
    ]
    
    todos_ok = True
    for modulo, nombre in modulos:
        try:
            __import__(modulo)
            print(f"{Colors.GREEN}  - {nombre}: OK{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}  - {nombre}: FALLO{Colors.END}")
            todos_ok = False
    
    return todos_ok

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

  ✅ Interfaz 100% terminal - Rapida y ligera
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

def crear_accesos_directos():
    """Crea accesos directos para cada sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        # Crear .bat para Windows
        with open('INICIAR_XONICHAT.bat', 'w') as f:
            f.write("""@echo off
title XONICHAT 2026 - Cliente Gemini para Terminal
color 1F
echo ========================================
echo      XONICHAT 2026 - Cliente Gemini
echo      Desarrollado por Darian Alberto
echo ========================================
echo.
python start.py
pause
""")
        print(f"{Colors.GREEN}Creado INICIAR_XONICHAT.bat - Haz doble clic para ejecutar{Colors.END}")
    
    elif sistema == 'linux':
        # Crear .sh para Linux
        with open('INICIAR_XONICHAT.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONICHAT 2026 - Cliente Gemini"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONICHAT.sh', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONICHAT.sh - Ejecuta con: ./INICIAR_XONICHAT.sh{Colors.END}")
    
    elif sistema == 'darwin':
        # Crear .command para Mac
        with open('INICIAR_XONICHAT.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONICHAT 2026 - Cliente Gemini"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONICHAT.command', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONICHAT.command - Haz doble clic para ejecutar{Colors.END}")

def main():
    """Funcion principal"""
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    # Verificar si hay argumentos de ayuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado{Colors.END}")
        print("Instala Python desde: https://www.python.org/downloads/")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    python_version = subprocess.run(get_python_command() + ['--version'], 
                                   capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Verificar pip e instalarlo si es necesario (solo Linux)
    if get_system() == 'linux' and not check_pip():
        print(f"\n{Colors.YELLOW}pip no esta instalado{Colors.END}")
        respuesta = input("¿Deseas instalar pip automaticamente? (s/n): ")
        if respuesta.lower() == 's':
            if install_pip_linux():
                print(f"{Colors.GREEN}pip instalado correctamente. Continuando...{Colors.END}")
            else:
                print(f"{Colors.RED}No se pudo instalar pip. Instalalo manualmente.{Colors.END}")
                input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
                return
        else:
            print("No se puede continuar sin pip. Instalalo manualmente.")
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
            return
    
    # Verificar dependencias
    faltantes = check_dependencies()
    
    if faltantes:
        print(f"\n{Colors.YELLOW}Faltan dependencias{Colors.END}")
        respuesta = input("Instalar automaticamente? (s/n): ")
        
        if respuesta.lower() == 's':
            if not install_dependencies(faltantes):
                print(f"\n{Colors.RED}No se pudieron instalar las dependencias{Colors.END}")
                input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
                return
        else:
            print(f"\nPuedes instalarlas manualmente con:")
            print("  pip install requests")
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
            return
    
    # Verificar archivo keys.txt
    verificar_archivo_keys()
    
    # Verificar que existe xonichat.py
    if not os.path.exists('xonichat.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonichat.py{Colors.END}")
        print("Asegurate de que xonichat.py esta en el mismo directorio")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar que las importaciones funcionan
    print(f"\n{Colors.BOLD}Verificando que todo funcione...{Colors.END}")
    if not verificar_importaciones():
        print(f"\n{Colors.RED}Error: No se puede importar requests{Colors.END}")
        print("El programa no puede continuar sin esta dependencia")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}Iniciando XONICHAT...{Colors.END}")
    print(f"{Colors.BOLD}Para salir en cualquier momento:{Colors.END} Ctrl+C o escribir /salir")
    print("-" * 60)
    
    # EJECUTAR xonichat.py
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonichat.py']
        print(f"Ejecutando: {' '.join(cmd)}")
        print("-" * 60)
        time.sleep(1)  # Pequeña pausa para leer el mensaje
        
        # Ejecutar xonichat.py
        resultado = subprocess.run(cmd)
        
        if resultado.returncode != 0:
            print(f"\n{Colors.RED}Error: xonichat.py termino con codigo {resultado.returncode}{Colors.END}")
            
    except FileNotFoundError:
        print(f"\n{Colors.RED}Error: No se encuentra xonichat.py{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programa detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonichat.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONICHAT 2026{Colors.END}")
    print(f"{Colors.BLUE}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    print(f"{Colors.BLUE}#Somos XONINDU{Colors.END}")
    
    # Pausa al final
    if get_system() != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        # Crear accesos directos
        crear_accesos_directos()
        
        # Ejecutar programa principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
