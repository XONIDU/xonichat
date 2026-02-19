# XONICHAT - Cliente Gemini para Terminal

Cliente de chat por terminal para Google Gemini, diseñado para ser ligero y funcionar en equipos de bajos recursos como ASUS Eee PC. Soporta múltiples API keys y cambio automático cuando una se agota.

## ⚡ Características

- ✅ Cliente 100% terminal - Interfaz ligera y rápida
- ✅ Soporte para Google Gemini (gratuito)
- ✅ Múltiples API keys con cambio automático
- ✅ Historial de conversación contextual
- ✅ Comandos intuitivos
- ✅ Optimizado para ASUS Eee PC y equipos de bajos recursos
- ✅ Sin dependencias pesadas

## 📦 Requisitos

- Python 3.6+
- pip (gestor de paquetes de Python)
- Conexión a internet
- API key de Google Gemini (gratuita)

## 🔧 Instalación

### 1. Instalar dependencias

```bash
# En antiX/Debian/Ubuntu
sudo apt update
sudo apt install python3 python3-pip
pip3 install requests

# En Arch Linux
sudo pacman -S python-pip
pip install requests

# En cualquier sistema con pip
pip install requests
```

### 2. Obtener API key de Gemini

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta Google
3. Haz clic en "Get API key" o "Crear API key"
4. Copia la key generada (comienza con `AIza...`)

### 3. Configurar XONICHAT

1. **Descarga el programa** (guarda el código como `xonichat.py`)

2. **Crea el archivo de keys**:
   ```bash
   nano keys.txt
   ```
   Agrega tus API keys (una por línea):
   ```
   AIzaSyCH5JpDDvI7gE87FN7iDUG5a78JFQeLXq4
   AIzaSyDYOETiQqB7od-Mzs_qC99vk9n4fcGFV0c
   ```

3. **Ejecuta**:
   ```bash
   python3 xonichat.py
   ```

## 🎮 Uso

### Comandos básicos

| Comando | Descripción |
|---------|-------------|
| `/help` | Muestra la ayuda |
| `/keys` | Lista las keys disponibles |
| `/key N` | Cambia a la key número N |
| `/clear` | Limpia la pantalla |
| `/reset` | Reinicia la conversación |
| `/hist` | Muestra el historial reciente |
| `/model` | Muestra el modelo actual |
| `/salir` | Sale del programa |

### Ejemplo de uso

```
==================================================
 XONICHAT - Gemini Edition
==================================================
Keys: 2 | Modelo: gemini-1.5-flash
Escribe /help para comandos

[G1/2] >>> Hola, ¿cómo estás?
[...] consultando Gemini...

[G1/2]: ¡Hola! Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?

[G1/2] >>> /keys

Keys disponibles: 2
-> [1] AIzaSyCH...LXq4
   [2] AIzaSyDY...FV0c

[G1/2] >>> /salir
XONICHAT - Hasta luego
```
## 📝 Archivo de configuración

### `keys.txt`
```
# Tus API keys de Gemini (una por línea)
# Las líneas que empiezan con # son ignoradas
AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********
AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********
```

## ⚠️ Límites gratuitos de Gemini

- **Gemini 1.5 Flash**: 60 solicitudes por minuto (gratis)
- **Gemini 1.5 Pro**: Límites más altos pero puede tener costo
- El programa cambia automáticamente de key cuando una alcanza el límite

## 🔍 Solución de problemas

### Error: "No hay keys válidas"
- Verifica que `keys.txt` exista y contenga keys válidas
- Las keys deben comenzar con `AIza...`

### Error: "Modelo no encontrado"
- El programa detecta automáticamente los modelos disponibles
- Puede deberse a una key inválida o sin acceso a Gemini

### Error de conexión
- Verifica tu conexión a internet
- Asegúrate de que la API de Gemini sea accesible en tu región

## 📁 Estructura de archivos

```
xonichat/
├── xonichat.py      # Programa principal
├── keys.txt         # API keys (crear manualmente)
└── README.md        # Este archivo
```

## 🤝 Contribuciones

Si encuentras bugs o quieres mejorar el programa:
1. Haz un fork del repositorio
2. Crea una rama con tu mejora
3. Envía un pull request

## 📧 Contacto

**Creador:** Darian Alberto Camacho Salas  
**Email:** xonidu@gmail.com  
**Proyecto:** XoniChat - Cliente Gemini para terminal

## 📄 Licencia

Este proyecto es de código abierto. Si lo usas, agradecería un crédito.
---

*Optimizado para ASUS Eee PC 900 con antiX Linux - 1GB RAM*
