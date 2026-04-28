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

## 🔑 Configuración

La primera vez que ejecutes `xonichat` se abrirá un gestor interactivo.

### Obtener API keys gratis
👉 https://aistudio.google.com/app/apikey

### Ubicación manual
```bash
~/.xonichat/keys.txt     # Una key por línea
```

---

## 🚀 Uso

```bash
xonichat
```

| Comando | Acción |
|---------|--------|
| Mensaje | Enviar a Gemini |
| `/salir` | Terminar sesión |
| `Ctrl+C` | Salir |

---

## 📁 Estructura del paquete

| Archivo | Ubicación |
|---------|-----------|
| `xonichat` | `/usr/bin/xonichat` |
| `xonichat.py` | `/usr/share/xonichat/` |
| `keys.txt` | `~/.xonichat/keys.txt` |

---

## 🐛 Problemas comunes

| Problema | Solución |
|----------|----------|
| `No valid keys` | Ejecuta `xonichat` y usa el gestor interactivo |
| `Permission denied` | Usa `~/.xonichat/keys.txt`, no `/usr/share/` |
| `No module 'requests'` | `pip install requests` |

---

## 📄 Licencia

MIT © Darian Alberto Camacho Salas

---

**Consulta de Gemini desde Terminal** 🚀

