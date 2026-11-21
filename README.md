# Calculadora IP (CIDR)

Aplicación de escritorio desarrollada en Python para el cálculo de subredes IPv4 (CIDR). 
Toda la lógica matemática está implementada manualmente mediante operaciones a nivel de bits (`&`, `|`, `~`, `<<`, `>>`), sin depender de módulos externos de red.

## Características
- Acepta direcciones en formato CIDR (`192.168.1.0/24`) o IP y máscara por separado (`192.168.1.0` y `255.255.255.0` o `/24`).
- Calcula dirección de red, rango de hosts utilizables, dirección de broadcast, máscara decimal, prefijo y total de hosts disponibles (incluyendo casos especiales `/31` y `/32`).
- Opción desplegable para visualizar la representación binaria de la red, máscara y broadcast.
- Validación de entradas con alertas de error en la interfaz gráfica.

## Estructura de archivos
```text
CalculadoraCIDR/
├── cidr.py          # Lógica matemática, validaciones y operaciones bit a bit
├── interfaz.py      # Interfaz gráfica de usuario (GUI) en Tkinter
├── .gitignore       # Archivos y carpetas ignorados por Git
└── README.md        # Documentación del proyecto# Calculadora IP (CIDR)

Aplicación de escritorio desarrollada en Python para el cálculo de subredes IPv4 (CIDR). 
Toda la lógica matemática está implementada manualmente mediante operaciones a nivel de bits (`&`, `|`, `~`, `<<`, `>>`), sin depender de módulos externos de red.

## Características
- **Entradas flexibles:** Acepta direcciones en formato CIDR (`192.168.1.0/24`) o IP y máscara por separado (`192.168.1.0` con `255.255.255.0`, `24` o `/24`).
- **Cálculos completos:** Obtiene dirección de red, rango de hosts utilizables, dirección de broadcast, máscara decimal, prefijo CIDR y total de hosts disponibles.
- **Casos especiales:** Maneja correctamente redes `/31` (enlaces punto a punto) y `/32` (host único).
- **Vista binaria opcional:** Permite desplegar u ocultar la representación en binario de la dirección de red, máscara y broadcast.
- **Validación de errores:** Verifica el formato de octetos, rangos numéricos y contigüidad de bits en la máscara, mostrando alertas claras en pantalla.

## Estructura de archivos
```text
CalculadoraCIDR/
├── cidr.py          # Lógica matemática, validaciones y operaciones bit a bit
├── interfaz.py      # Interfaz gráfica de usuario (GUI) en Tkinter
├── .gitignore       # Archivos y carpetas ignorados por Git (ej. venv/)
└── README.md        # Documentación del proyecto
```

## Dependencias
- **Python 3.10 o superior**
- **Tkinter:** Incluido en la librería estándar de Python (usado en `interfaz.py`).
- **Módulo local `cidr.py`:** Importado directamente por `interfaz.py`; no requiere librerías externas.

### Dependencias opcionales (desarrollo)
- `pytest`: Para ejecutar pruebas unitarias de la lógica matemática.
- `pyinstaller`: Para empaquetar la aplicación como ejecutable independiente (`.exe`).

## Cómo ejecutar el proyecto
1. Clona el repositorio y entra a la carpeta del proyecto:
   ```bash
   git clone https://github.com/EmmaBlackPH/CalculadoraCIDR.git
   cd CalculadoraCIDR
   ```
2. Ejecuta la interfaz gráfica:
   ```bash
   python interfaz.py
   ```

## Ejemplos de uso

### Formatos de entrada aceptados
| Campo: IP o IP/Prefijo | Campo: Máscara (opcional) | Resultado            |
| `192.168.1.45/24`      | *(vacío)*                 | Red `192.168.1.0/24` |
| `192.168.1.45`         | `255.255.255.0`           | Red `192.168.1.0/24` |
| `192.168.1.45`         | `24` o `/24`              | Red `192.168.1.0/24` |

### Ejemplo de salida (`192.168.1.45/24`)
- **Dirección de Red:** `192.168.1.0`
- **Rango de Hosts:** `192.168.1.1 — 192.168.1.254`
- **Dirección Broadcast:** `192.168.1.255`
- **Máscara Decimal:** `255.255.255.0`
- **Prefijo CIDR:** `/24`
- **Hosts Disponibles:** `254`
- **Red (en binario):** `11000000.10101000.00000001.00000000`
- **Máscara (en binario):** `11111111.11111111.11111111.00000000`
- **Broadcast (en binario):** `11000000.10101000.00000001.11111111`