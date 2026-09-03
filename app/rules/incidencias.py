from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

TOLERANCIA_ATRASO_MIN = 10
UMBRAL_REVISION_RETRASO_MIN = 60
UMBRAL_INFORMATIVO_MIN = 30
PAUSA_COMIDA_MIN = 30
PAUSA_COMIDA_MINIMA = 20
PAUSA_COMIDA_MAXIMA = 45

LICENCIAS_PAGADAS = {
    "BAJA_MEDICA", "PERMISO_CON_GOCE", "VACACIONES",
    "LICENCIA_MATERNIDAD", "LICENCIA_PATERNIDAD", "DUELO_FAMILIAR",
    "REDUCCION_LACTANCIA", "LACTANCIA", "MATERNIDAD",
}
FALTAS_JUSTIFICADAS = {"PERMISO_SIN_GOCE", "FALTA_JUSTIFICADA"}


@dataclass(frozen=True)
class ResultadoIncidencia:
    tipo: str
    impacto: str
    consecuencia_por_defecto: str
    requiere_decision: bool = True


def es_descanso_semanal(fecha: date, turno: str) -> bool:
    turno_nocturno = "NOCTURN" in str(turno).upper()
    return fecha.weekday() == (5 if turno_nocturno else 6)


def consecuencia_sin_marcacion(
    fecha: date,
    turno: str,
    novedad: str | None = None,
    es_staff: bool = False,
) -> str:
    novedad = str(novedad or "").strip().upper()
    if es_staff:
        return "NORMAL_STAFF"
    if novedad in LICENCIAS_PAGADAS:
        return "AUSENCIA_JUSTIFICADA_PAGADA"
    if novedad in FALTAS_JUSTIFICADAS:
        return "FALTA_JUSTIFICADA"
    if es_descanso_semanal(fecha, turno):
        return "DESCANSO_SEMANAL"
    return "FALTA_INJUSTIFICADA"


def incidencia_horaria(tipo: str, minutos: int) -> ResultadoIncidencia:
    tipo = tipo.upper()
    minutos = max(0, int(minutos))
    if tipo in {"ENTRADA_TEMPRANA", "SALIDA_TARDE"}:
        return ResultadoIncidencia(tipo, "INFORMATIVO", "NORMAL")
    if tipo == "ENTRADA_TARDE":
        if minutos <= TOLERANCIA_ATRASO_MIN:
            return ResultadoIncidencia(tipo, "INFORMATIVO", "NORMAL", False)
        return ResultadoIncidencia(tipo, "AUTOMATICO", f"ATRASO_{minutos}_MIN", False) if minutos <= UMBRAL_REVISION_RETRASO_MIN else ResultadoIncidencia(tipo, "PENDIENTE", f"ATRASO_{minutos}_MIN")
    if tipo == "SALIDA_TEMPRANA":
        if minutos <= TOLERANCIA_ATRASO_MIN:
            return ResultadoIncidencia(tipo, "INFORMATIVO", "NORMAL", False)
        if minutos <= 30:
            return ResultadoIncidencia(tipo, "AUTOMATICO", f"SALIDA_TEMPRANA_{minutos}_MIN", False)
        return ResultadoIncidencia(tipo, "PENDIENTE", "SALIDA_TEMPRANA")
    raise ValueError(f"Tipo de incidencia no soportado: {tipo}")


def incidencia_marcacion_incompleta() -> ResultadoIncidencia:
    return ResultadoIncidencia(
        "MARCACION_INCOMPLETA", "PENDIENTE", "FALTA_INJUSTIFICADA"
    )


def incidencia_comida(pausa_minutos: int | None, horas_trabajadas: float) -> ResultadoIncidencia | None:
    if horas_trabajadas < 6:
        return None
    if pausa_minutos is None:
        return ResultadoIncidencia("SIN_MARCACION_COMIDA", "PENDIENTE", "NORMAL")
    if PAUSA_COMIDA_MINIMA <= pausa_minutos <= PAUSA_COMIDA_MAXIMA:
        return None
    return ResultadoIncidencia(
        "PAUSA_COMIDA_IRREGULAR", "PENDIENTE", "NORMAL"
    )


def posible_turno_y_medio(
    tipo_personal: str,
    turno: str,
    dia_semana: int,
    entrada_hora: int,
) -> ResultadoIncidencia | None:
    if "JORNAL" not in str(tipo_personal).upper():
        return None
    if "NOCTURN" not in str(turno).upper():
        return None
    if dia_semana not in {4, 6}:
        return None
    if not 16 <= entrada_hora <= 19:
        return None
    return ResultadoIncidencia(
        "POSIBLE_TURNO_Y_MEDIO", "PENDIENTE", "TURNO_NORMAL"
    )


def resolver(incidencia: ResultadoIncidencia, decision: str | None) -> str:
    decision = str(decision or "").strip().upper()
    if not decision or decision == "PENDIENTE":
        return (
            "NORMAL"
            if incidencia.impacto == "INFORMATIVO"
            else incidencia.consecuencia_por_defecto
        )
    mapa = {
        "APROBADO": "NORMAL",
        "APROBADO_HE": "NORMAL_CON_HE_APROBADA",
        "JUSTIFICAR_FALTA": "FALTA_JUSTIFICADA",
        "VALIDAR_TRABAJADO": "DIA_TRABAJADO",
        "APROBAR_TURNO_Y_MEDIO": "TURNO_Y_MEDIO",
        "RECHAZADO": incidencia.consecuencia_por_defecto,
    }
    if decision not in mapa:
        raise ValueError(f"Decisión no soportada: {decision}")
    return mapa[decision]


def consolidar(incidencias: Iterable[ResultadoIncidencia]) -> dict:
    items = list(incidencias)
    pendientes = [i for i in items if i.impacto == "PENDIENTE"]
    return {
        "tipos": " | ".join(dict.fromkeys(i.tipo for i in items)),
        "impacto": "PENDIENTE" if pendientes else "INFORMATIVO",
        "consecuencia_por_defecto": (
            pendientes[0].consecuencia_por_defecto if pendientes else "NORMAL"
        ),
    }
