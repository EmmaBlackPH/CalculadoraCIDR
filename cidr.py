"""
Módulo: cidr.py
Descripción: Lógica matemática y operaciones bit a bit para cálculo de subredes IPv4.
Dependencias: Ninguna (solo librería estándar de Python 3).
"""
# Esta función valida una dirección IPv4 y la convierte a un entero de 32 bits.
# Verifica primero que la direccion IP tenga exactamente 4 octetos y que cada octeto sea un numero entero entre 0 y 255. 
# Luego, convierte cada octeto a su representación binaria y los combina en un solo entero de 32 bits.
def ip_a_entero(ip: str) -> int:
    partes = ip.strip().split(".")
    if len(partes) != 4:
        raise ValueError("La dirección IP debe tener exactamente 4 octetos (ej. 192.168.1.0).")
    resultado = 0
    for parte in partes:
        if not parte.isdigit():
            raise ValueError(f"Octeto inválido '{parte}': solo se permiten números enteros positivos.")
        octeto = int(parte)
        if octeto < 0 or octeto > 255:
            raise ValueError(f"Octeto fuera de rango ({octeto}): cada octeto debe estar entre 0 y 255.")
        resultado = (resultado << 8) | octeto
    return resultado

# Convierte un entero de 32 bits a formato IPv4 decimal punteado.
# Toma el numero entero de 32 bits y lo desplaza a la derecha para extraer cada octeto, 
# luego los convierte a string y los une con puntos.
def entero_a_ip(numero: int) -> str:
    return ".".join(str((numero >> (8 * i)) & 255) for i in (3, 2, 1, 0))

# Convierte un entero de 32 bits a representación binaria separada por puntos.
# Toma el numero entero de 32 bits y lo desplaza a la derecha para extraer cada octeto, 
# luego los convierte a binario con 8 bits y los une con puntos.
def entero_a_binario(numero: int) -> str:
    return ".".join(f"{(numero >> (8 * i)) & 255:08b}" for i in (3, 2, 1, 0))

# Convierte un prefijo (0-32) a una máscara entera de 32 bits.
# La máscara se calcula desplazando 1's a la izquierda y llenando con 0's a la derecha.
def prefijo_a_mascara_int(prefijo: int) -> int:
    if not isinstance(prefijo, int) or prefijo < 0 or prefijo > 32:
        raise ValueError("El prefijo debe ser un número entero entre 0 y 32.")
    if prefijo == 0:
        return 0
    return (0xFFFFFFFF << (32 - prefijo)) & 0xFFFFFFFF

# Valida una máscara decimal punteada (ej. 255.255.255.0) y devuelve su prefijo /n.
# Primero convierte la mascara a un entero, luego a binario y verifica que los bits en 1 esten juntos.
def mascara_a_prefijo(mascara: str) -> int:
    mascara_int = ip_a_entero(mascara)
    binario = f"{mascara_int:032b}"
    # Una mascara valida no puede tener un '1' después de un '0'
    if "01" in binario:
        raise ValueError(f"La máscara '{mascara}' no es válida (sus bits en 1 deben ser contiguos).")
    return binario.count("1")

#  Calcula todos los datos CIDR a partir de:
#    - entrada_ip con prefijo (ej. '192.168.1.0/24')
#    - entrada_ip y entrada_mascara (ej. '192.168.1.0' y '255.255.255.0' o '24')
#  Devuelve un diccionario con los resultados en formato decimal y binario.

def calcular_cidr(entrada_ip: str, entrada_mascara: str = "") -> dict:
    entrada_ip = entrada_ip.strip()
    entrada_mascara = entrada_mascara.strip()
    if not entrada_ip:
        raise ValueError("Debes ingresar una dirección IP.")
    # Determinar IP y prefijo según cómo los ingresó el usuario
    if "/" in entrada_ip:
        partes = entrada_ip.split("/")
        if len(partes) != 2 or not partes[1].isdigit():
            raise ValueError("Formato CIDR inválido. Usa el formato IP/prefijo (ej. 192.168.1.0/24).")
        ip = partes[0]
        prefijo = int(partes[1])
    else:
        ip = entrada_ip
        if not entrada_mascara:
            raise ValueError("Ingresa el prefijo en la IP (ej. /24) o escribe la máscara en el segundo campo.")
        if entrada_mascara.startswith("/"):
            entrada_mascara = entrada_mascara[1:]
        if entrada_mascara.isdigit():
            prefijo = int(entrada_mascara)
        else:
            prefijo = mascara_a_prefijo(entrada_mascara)
    ip_int = ip_a_entero(ip)
    mascara_int = prefijo_a_mascara_int(prefijo)
    # Operaciones bit a bit fundamentales
    red_int = ip_int & mascara_int # AND: conserva bits de red y apaga los de host
    wildcard_int = (~mascara_int) & 0xFFFFFFFF  # NOT + recorte a 32 bits: invierte la máscara (wildcard)
    broadcast_int = red_int | wildcard_int   # OR: enciende en 1 todos los bits de host
    # Cálculo de hosts disponibles y rango 
    if prefijo == 32:
        hosts_disponibles = 1
        rango_hosts = f"{entero_a_ip(red_int)} (host único)"
    elif prefijo == 31:
        hosts_disponibles = 2
        rango_hosts = f"{entero_a_ip(red_int)} — {entero_a_ip(broadcast_int)} (enlace punto a punto)"
    else:
        hosts_disponibles = (2 ** (32 - prefijo)) - 2
        primer_host = entero_a_ip(red_int + 1)
        ultimo_host = entero_a_ip(broadcast_int - 1)
        rango_hosts = f"{primer_host} — {ultimo_host}"
    return {
        "ip_ingresada": entero_a_ip(ip_int),
        "red": entero_a_ip(red_int),
        "rango_hosts": rango_hosts,
        "broadcast": entero_a_ip(broadcast_int),
        "mascara_decimal": entero_a_ip(mascara_int),
        "prefijo": f"/{prefijo}",
        "hosts_disponibles": hosts_disponibles,
        "binario": {
            "red": entero_a_binario(red_int),
            "mascara": entero_a_binario(mascara_int),
            "broadcast": entero_a_binario(broadcast_int),
        },
    }