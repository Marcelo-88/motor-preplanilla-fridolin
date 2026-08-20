import pandas as pd

from app.processors.validar_datos import (
    normalizar_ci,
    separar_biometrico_no_identificado,
    validar_maestro,
)


def test_normalizar_ci_permite_letras_y_quita_espacios():
    assert normalizar_ci(" ab 123 ") == "AB123"
    assert normalizar_ci("123.0") == "123"


def test_sin_supervisor_no_excluye():
    maestro = pd.DataFrame([
        {"CI": "A1", "Nombre_Completo": "Ana", "Tipo_Personal": "FIJO", "Supervisor": ""}
    ])
    resultado = validar_maestro(maestro)
    assert len(resultado.maestro_valido) == 1
    assert len(resultado.advertencias) == 1


def test_sin_tipo_excluye():
    maestro = pd.DataFrame([
        {"CI": "A1", "Nombre_Completo": "Ana", "Tipo_Personal": "", "Supervisor": "S1"}
    ])
    resultado = validar_maestro(maestro)
    assert len(resultado.maestro_valido) == 0
    assert resultado.maestro_excluido.iloc[0]["MOTIVO_EXCLUSION"] == "SIN_TIPO_PERSONAL"


def test_biometrico_no_identificado_se_separa():
    maestro = pd.DataFrame([
        {"CI": "A1", "Nombre_Completo": "Ana", "Tipo_Personal": "FIJO", "Supervisor": "S1"}
    ])
    resultado = validar_maestro(maestro)
    biometrico = pd.DataFrame([{"CI": "A1"}, {"CI": "B2"}])
    vinculado, no_identificado = separar_biometrico_no_identificado(
        biometrico, resultado.maestro_valido
    )
    assert len(vinculado) == 1
    assert len(no_identificado) == 1
    assert no_identificado.iloc[0]["MOTIVO"] == "CI_NO_EXISTE_EN_MAESTRO_VALIDO"
