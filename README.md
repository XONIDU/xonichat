# 🤖 XONICHAT

**Advertencia:** Este código tiene fines educativos y de investigación. Debe usarse de manera responsable. El autor no se hace responsable del uso indebido.

## 🎯 ¿Qué es XONICHAT?

XONICHAT es un cliente de inteligencia artificial por terminal que permite interactuar con el modelo Gemini de Google desde equipos de cómputo de bajos recursos. Consta de dos componentes:

- **start.py** - Lanzador universal que verifica dependencias y ejecuta el programa principal
- **xonichat.py** - Programa principal con el cliente de Gemini

Está especialmente diseñado para funcionar en equipos de bajos recursos como ASUS Eee PC, Raspberry Pi, y dispositivos con recursos limitados.

### Características principales:
- ✅ Interfaz 100% terminal - Rápida y ligera
- ✅ Múltiples API keys - Cambio automático cuando una se agota
- ✅ Historial de conversación - Contexto entre mensajes
- ✅ Optimizado - Funciona en ASUS Eee PC y equipos similares
- ✅ Manejo de errores robusto
- ✅ Pruebas automatizadas incluidas

---

## 📥 Instalación

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/XONIDU/xonichat.git
cd xonichat
```

---

## ✅ Requisitos

- Python 3.6+ instalado
- Conexión a Internet
- API key de Google Gemini (gratuita)
- Dependencias Python listadas en `requirements.txt`

---

## 🔑 Obtención de API Keys

1. Ve a: https://aistudio.google.com/app/apikey
2. Inicia sesión con tu cuenta Google
3. Crea una nueva API key
4. Copia la key (comienza con `AIzaSy...`)

---

## 📦 Instalación de dependencias por plataforma

### 🐧 Arch Linux / Manjaro

```bash
# Instalar dependencias del sistema
sudo pacman -S python-pip

# Instalar dependencias Python
pip install -r requirements.txt --break-system-packages
```

### 🐧 Ubuntu / Debian / antiX

```bash
# Actualizar repositorios
sudo apt update

# Instalar dependencias del sistema
sudo apt install python3 python3-pip -y

# Instalar dependencias Python
pip3 install -r requirements.txt --break-system-packages
```

### 🍎 macOS

```bash
# Instalar dependencias Python
pip3 install -r requirements.txt
```

### 🪟 Windows

1. Instala Python 3 desde [python.org](https://python.org)
2. Abre una terminal (cmd o PowerShell) y ejecuta:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración

Crea un archivo `keys.txt` en la misma carpeta con tus API keys (una por línea):

```txt
# Tus API keys de Gemini (una por línea)
AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********
AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********
```

El programa soporta múltiples keys y cambia automáticamente cuando una se agota.

---

## 🚀 Uso

Ejecuta el lanzador:

```bash
python start.py
# o
python3 start.py
```

El lanzador verificará las dependencias y automáticamente ejecutará `xonichat.py`.

### Comandos disponibles:

- Escribe tu mensaje y presiona Enter para enviarlo
- Escribe `/salir` para terminar la conversación
- `Ctrl+C` para salir del programa

### Ejemplo de sesión:

```
$ python start.py

============================================================
                    XONICHAT 2026 v4.2.0
============================================================
 Keys: 2 | Modelo: gemini-2.5-flash
============================================================

[G1/2] >>> Hola, ¿cómo estás?
[...] Consultando Gemini...

[G1/2]: ¡Hola! Estoy bien, gracias por preguntar. Soy Gemini, un modelo de lenguaje creado por Google. ¿En qué puedo ayudarte hoy?
```

---

## 📁 Archivos del proyecto

- `start.py` — Lanzador universal (verifica dependencias y ejecuta el programa)
- `xonichat.py` — Programa principal con el cliente de Gemini
- `keys.txt` — Archivo de configuración de API keys (crear manualmente)
- `requirements.txt` — Dependencias Python
- `start_test.py` — Pruebas automatizadas
- `README.md` — Este archivo de documentación
- `LICENSE` — Licencia MIT

---

## 🧪 Pruebas automatizadas

XONICHAT incluye un conjunto de pruebas unitarias para verificar su correcto funcionamiento:

```bash
python start_test.py
```

---

## 🔄 Rotación automática de keys

Una de las características más importantes de XONICHAT es su capacidad para manejar múltiples API keys:

1. Comienza usando la primera key
2. Si recibe un error 429 (límite de cuota excedido), cambia automáticamente a la siguiente
3. Continúa rotando hasta encontrar una key funcional
4. Muestra qué key está activa con el indicador `[G1/2]`, `[G2/2]`, etc.

---

## ✋ Pausar / Detener

- Para detener el programa: `Ctrl+C` o escribir `/salir`
- El programa guarda automáticamente el historial de comandos

---

## 🔒 Consideraciones de seguridad y ética

- No compartas tus API keys públicamente
- Las keys en `keys.txt` deben mantenerse privadas
- Este programa es SOLO para fines educativos y de investigación
- Úsalo de manera responsable y respeta los términos de servicio de Google

---

## 🐛 Problemas comunes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'requests'` | Ejecuta: `pip install requests` |
| `[ERROR] keys.txt not found` | Crea el archivo `keys.txt` con tus API keys |
| `[ERROR] No valid keys in keys.txt` | Verifica que las keys sean válidas y estén bien escritas |
| Error 429 (quota exceeded) | El programa cambiará automáticamente a la siguiente key |
| Error en Linux con permisos | Usa `pip install --user` si no tienes permisos de root |

---

## 📊 Estadísticas del proyecto

- ⭐ Estrellas: 0
- 👀 Observadores: 1
- 🍴 Forks: 0
- 🏷️ Releases: 1 (v4.2.0)
- 🐍 Lenguaje principal: Python 100.0%

---

## 📄 Licencia

MIT License - Ver archivo [LICENSE](LICENSE)

---

## ✉️ Contacto y Créditos

- **Proyecto:** XONICHAT
- **Contacto:** xonidu@gmail.com
- **Creador:** Darian Alberto Camacho Salas
- **GitHub:** [@XONIDU](https://github.com/XONIDU)
- **#Somos XONINDU**

---

