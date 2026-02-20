# XONICHAT - Cliente Gemini para Terminal

Cliente de chat por terminal para Google Gemini, diseñado para ser ligero y funcionar en equipos de bajos recursos. Soporta múltiples API keys y cambio automático cuando una se agota.

## Características

- Cliente 100% terminal - Interfaz ligera y rápida
- Soporte para Google Gemini
- Múltiples API keys con cambio automático
- Historial de conversación contextual
- Optimizado para equipos de bajos recursos
- Sin dependencias pesadas

## Requisitos

- Python 3.6+
- pip (gestor de paquetes de Python)
- Conexión a internet
- API key de Google Gemini

## Instalación

### 1. Instalar dependencias

```
# En antiX/Debian/Ubuntu
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install requests

# En Arch Linux
sudo pacman -S python-pip
pip install requests

# En cualquier sistema con pip
pip install requests
```

### 2. Obtener API key de Gemini

Las API keys se obtienen gratuitamente en:
https://aistudio.google.com/app/apikey

### 3. Configurar XONICHAT

1. Guarda el codigo como `xonichat.py`
2. Crea el archivo `keys.txt` en la misma carpeta
3. Agrega tus API keys (una por linea)

### 4. Ejecutar
python3 start.py

## Uso

- Escribe tu mensaje y presiona Enter
- Escribe `/salir` para terminar la conversacion
- El programa cambia automaticamente de key cuando una se agota

## Archivos

- `start.py` - Programa principal
- `keys.txt` - API keys (crear manualmente)

## Creditos

**BY: XONIDU - Darian Alberto Camacho Salas**

## Contacto

Email: xonidu@gmail.com

## Licencia

Proyecto de codigo abierto.

---

*Optimizado para ASUS Eee PC y equipos de bajos recursos*

