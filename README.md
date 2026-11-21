# Calculadora IP (CIDR)

Aplicación de escritorio desarrollada en Python para el cálculo de subredes IPv4 (CIDR). Toda la lógica matemática está implementada manualmente mediante operaciones a nivel de bits (`&`, `|`, `~`, `<<`, `>>`), sin depender de módulos externos de red.

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
├── test_cidr.py     # Pruebas unitarias con pytest para validar la lógica CIDR
├── .gitignore       # Archivos y carpetas ignorados por Git (venv/, caché, build/)
└── README.md        # Documentación del proyecto
```

## Dependencias
- **Python 3.10 o superior**
- **Tkinter:** Incluido en la librería estándar de Python (usado en `interfaz.py`).
- **Módulo local `cidr.py`:** Importado directamente por `interfaz.py` y `test_cidr.py`; no requiere librerías externas.

### Dependencias opcionales (desarrollo)
- `pytest`: Para ejecutar la suite de pruebas unitarias (`test_cidr.py`).
- `pyinstaller`: Para empaquetar la aplicación como ejecutable independiente (`.exe`).

## Cómo ejecutar el proyecto
1. Clona el repositorio y entra a la carpeta del proyecto:
   ```bash
   git clone [https://github.com/EmmaBlackPH/CalculadoraCIDR.git](https://github.com/EmmaBlackPH/CalculadoraCIDR.git)
   cd CalculadoraCIDR
   ```
2. Ejecuta la interfaz gráfica:
   ```bash
   python interfaz.py
   ```

## Pruebas unitarias
El archivo `test_cidr.py` valida cálculos estándar (`/24`), subredes fuera de límite de octeto (`/26`), 
entradas separadas, casos especiales (`/31` y `/32`) y el manejo de errores ante entradas inválidas.

Para ejecutarlas:
```bash
pip install pytest
pytest -v
```

## Ejemplos de uso

### Formatos de entrada aceptados
| Campo: IP o IP/Prefijo | Campo: Máscara (opcional) | Resultado |
| :--- | :--- | :--- |
| `192.168.1.45/24` | *(vacío)* | Red `192.168.1.0/24` |
| `192.168.1.45` | `255.255.255.0` | Red `192.168.1.0/24` |
| `192.168.1.45` | `24` o `/24` | Red `192.168.1.0/24` |

### Ejemplo de salida (`192.168.1.45/24`)
- **Dirección de Red:** `192.168.1.0`
- **Rango de Hosts:** `192.168.1.1 — 192.168.1.254`
- **Dirección Broadcast:** `192.168.1.255`
- **Máscara Decimal:** `255.255.255.0`
- **Prefijo CIDR:** `/24`
- **Hosts Disponibles:** `254`
- **Red (bin):** `11000000.10101000.00000001.00000000`
- **Máscara (bin):** `11111111.11111111.11111111.00000000`
- **Broadcast (bin):** `11000000.10101000.00000001.11111111`