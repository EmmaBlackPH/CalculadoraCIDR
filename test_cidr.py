"""
Módulo: test_cidr.py
Descripción: Pruebas unitarias para validar la lógica matemática y el manejo de errores de cidr.py.
Dependencias: pytest y cidr.py (módulo local).
"""
import pytest
from cidr import calcular_cidr

# Verifica un cálculo estándar /24 incluyendo su representación binaria.
def test_red_estandar_24():
    res = calcular_cidr("192.168.1.45/24")
    assert res["red"] == "192.168.1.0"
    assert res["broadcast"] == "192.168.1.255"
    assert res["rango_hosts"] == "192.168.1.1 — 192.168.1.254"
    assert res["mascara_decimal"] == "255.255.255.0"
    assert res["prefijo"] == "/24"
    assert res["hosts_disponibles"] == 254
    assert res["binario"]["red"] == "11000000.10101000.00000001.00000000"
    assert res["binario"]["mascara"] == "11111111.11111111.11111111.00000000"
    assert res["binario"]["broadcast"] == "11000000.10101000.00000001.11111111"

# Verifica el cálculo con una máscara que no cae en límite de octeto (/26).
def test_subred_prefijo_26():
    res = calcular_cidr("10.0.0.130/26")
    assert res["red"] == "10.0.0.128"
    assert res["broadcast"] == "10.0.0.191"
    assert res["rango_hosts"] == "10.0.0.129 — 10.0.0.190"
    assert res["mascara_decimal"] == "255.255.255.192"
    assert res["hosts_disponibles"] == 62

# Verifica que funcione enviando IP y máscara (decimal o prefijo) por separado.
def test_entradas_separadas():
    res_decimal = calcular_cidr("172.16.5.10", "255.255.0.0")
    res_prefijo = calcular_cidr("172.16.5.10", "/16")
    assert res_decimal["red"] == "172.16.0.0"
    assert res_decimal["hosts_disponibles"] == 65534
    assert res_decimal == res_prefijo

# Verifica los casos especiales /31 (punto a punto) y /32 (host único).
def test_casos_especiales_31_y_32():
    res_31 = calcular_cidr("192.168.10.0/31")
    assert res_31["hosts_disponibles"] == 2
    assert res_31["rango_hosts"] == "192.168.10.0 — 192.168.10.1 (enlace punto a punto)"

    res_32 = calcular_cidr("8.8.8.8/32")
    assert res_32["hosts_disponibles"] == 1
    assert res_32["rango_hosts"] == "8.8.8.8 (host único)"


def test_errores_validacion():
    """Verifica que las entradas inválidas lancen ValueError correctamente."""
    with pytest.raises(ValueError):
        calcular_cidr("300.168.1.1/24")       # Octeto fuera de rango
    with pytest.raises(ValueError):
        calcular_cidr("192.168.1.1/33")       # Prefijo mayor a 32
    with pytest.raises(ValueError):
        calcular_cidr("192.168.1.1", "255.0.255.0")  # Máscara no contigua
    with pytest.raises(ValueError):
        calcular_cidr("192.168.1.1")          # Falta máscara o prefijo
    with pytest.raises(ValueError):
        calcular_cidr("")                     # Entrada vacía