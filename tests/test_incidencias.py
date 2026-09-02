from datetime import date

from app.rules.incidencias import (
    ResultadoIncidencia,
    consecuencia_sin_marcacion,
    incidencia_horaria,
    posible_turno_y_medio,
    resolver,
)


def test_informativo_sin_accion_procede_normal():
    i = incidencia_horaria("SALIDA_TARDE", 65)
    assert i.impacto == "INFORMATIVO"
    assert resolver(i, "PENDIENTE") == "NORMAL"


def test_pendiente_sin_accion_conserva_sancion():
    i = incidencia_horaria("ENTRADA_TARDE", 25)
    assert i.impacto == "PENDIENTE"
    assert resolver(i, None) == "ATRASO_25_MIN"


def test_sin_marcacion_aplica_falta_en_dia_laboral():
    assert consecuencia_sin_marcacion(date(2026, 8, 3), "Diurno") == "FALTA_INJUSTIFICADA"


def test_descanso_semanal_depende_del_turno():
    assert consecuencia_sin_marcacion(date(2026, 8, 2), "Diurno") == "DESCANSO_SEMANAL"
    assert consecuencia_sin_marcacion(date(2026, 8, 1), "Nocturno") == "DESCANSO_SEMANAL"


def test_turno_y_medio_nunca_se_aprueba_automaticamente():
    i = posible_turno_y_medio("Jornalero", "Nocturno", 4, 18)
    assert i is not None
    assert resolver(i, None) == "TURNO_NORMAL"
    assert resolver(i, "APROBAR_TURNO_Y_MEDIO") == "TURNO_Y_MEDIO"
