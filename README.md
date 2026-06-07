# 🤖 XONICHAT

Cliente Gemini por terminal optimizado para equipos de bajos recursos (ASUS Eee PC, Raspberry Pi, etc.)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AUR version](https://img.shields.io/aur/version/xonichat)](https://aur.archlinux.org/packages/xonichat)

---

## 📋 Características

- ✅ Interfaz 100% terminal - Rápida y ligera
- ✅ Múltiples API keys - Cambio automático cuando una se agota
- ✅ Historial de conversación - Contexto entre mensajes
- ✅ Gestor interactivo de keys - Sin necesidad de editar archivos
- ✅ Sin sudo - Las keys se guardan en `~/.xonichat/`

---

## 📦 Instalación

### Desde AUR (recomendado)

```bash
yay -S xonichat
```

### Manual desde GitHub

```bash
git clone https://github.com/XONIDU/xonichat.git
cd xonichat
pip install -r requirements.txt
python start.py
```

---

### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonicli"
```

Luego simplemente escribe:

```bash
xoninstall xonichat
cd xonichat
pip install -r requisitos.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xonicli`).

---

## 🔑 Configuración

La primera vez que ejecutes `xonichat` se abrirá un gestor interactivo.

### Obtener API keys gratis

👉 https://aistudio.google.com/app/apikey

### Ubicación manual

```bash
~/.xonichat/keys.txt     # Una key por línea
```

Formato del archivo:
```txt
AIzaSyCH5JpDDvI7gE87FN7iDUG5a78********
AIzaSyDYOETiQqB7od-Mzs_qC99vk9n********
```

---

## 🚀 Uso

```bash
xonichat
```

| Comando | Acción |
|---------|--------|
| Escribe tu mensaje | Enviar a Gemini |
| `/salir` | Terminar sesión |
| `Ctrl+C` | Salir del programa |

### Ejemplo de sesión

```
$ xonichat

============================================================
                    XONICHAT 2026 v4.2.8
============================================================
 Keys: 2 | Model: gemini-2.5-flash
 Keys file: /home/usuario/.xonichat/keys.txt
============================================================

[G1/2] >>> Hola, ¿cómo estás?
[...] Consultando Gemini...

[G1/2]: ¡Hola! Estoy bien, gracias por preguntar. ¿En qué puedo ayudarte?
```

---

## 📁 Estructura del paquete

| Archivo | Ubicación |
|---------|-----------|
| `xonichat` | `/usr/bin/xonichat` |
| `xonichat.py` | `/usr/share/xonichat/` |
| `keys.txt` | `~/.xonichat/keys.txt` |
| `README.md` | `/usr/share/doc/xonichat/` |
| `LICENSE` | `/usr/share/licenses/xonichat/` |

---

## 🔄 Rotación automática de keys

XONICHAT soporta múltiples API keys:

1. Comienza usando la primera key
2. Si recibe error 429 (límite de cuota), cambia automáticamente a la siguiente
3. Muestra qué key está activa con el indicador `[G1/2]`, `[G2/2]`, etc.

---

## 🧪 Pruebas

```bash
python start_test.py
```

---

## 🐛 Problemas comunes

| Problema | Solución |
|----------|----------|
| `No valid keys` | Ejecuta `xonichat` y usa el gestor interactivo |
| `Permission denied` | Usa `~/.xonichat/keys.txt`, no `/usr/share/` |
| `No module 'requests'` | `pip install requests` |
| Error 404 o 400 | Verifica tu conexión a Internet |

---

## 📄 Licencia

MIT © Darian Alberto Camacho Salas (XONIDU)

---

## ✉️ Contacto

- **Creador:** Darian Alberto Camacho Salas
- **Email:** xonidu@gmail.com
- **GitHub:** [@XONIDU](https://github.com/XONIDU)

---

