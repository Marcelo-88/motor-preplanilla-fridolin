from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime, time, timedelta
from typing import Iterable

TOLERANCIA_MIN = 10
COMIDA_MIN = 30
REVISION_RETRASO_MIN = 60


def norm_ci(value) -> str:
    text = str(value or "").strip().upper().replace(" ", "")
    return text[:-2] if text.endswith(".0") else text


@dataclass
class Punch:
    dt: datetime
    tipo: str
    raw: str = ""


@dataclass
class Jornada:
    fecha: date
    turno: str
    punches: list[Punch]
    entrada: datetime | None
    salida: datetime | None
    comida_min: int
    retraso_entrada: int
    retraso_comida: int
    salida_temprana_auto: int
    salida_temprana_pendiente: int
    salida_tardia: int
    total_retraso: int
    horas: float
    estado: str
    impacto: str
    consecuencia: str
    incidencias: list[str]
    auditoria: list[str]


def fecha_operativa(dt: datetime, turno: str) -> date:
    if "NOCTURN" in str(turno).upper() and dt.time() < time(12):
        return dt.date() - timedelta(days=1)
    return dt.date()


def _dedup(punches: Iterable[Punch]) -> list[Punch]:
    out: list[Punch] = []
    for p in sorted(punches, key=lambda x: x.dt):
        p.tipo = str(p.tipo or "").strip().upper()
        if out and p.tipo == out[-1].tipo and (p.dt - out[-1].dt).total_seconds() < 120:
            continue
        out.append(p)
    return out


def reconstruir(fecha: date, turno: str, punches: Iterable[Punch], es_descanso=False,
                novedad="", es_staff=False) -> Jornada:
    ps = _dedup(punches)
    audit: list[str] = []
    entradas = [p for p in ps if "ENTRADA" in p.tipo]
    salidas = [p for p in ps if "SALIDA" in p.tipo]
    if not ps:
        if es_descanso or es_staff or novedad:
            return Jornada(fecha, turno, [], None, None, 0,0,0,0,0,0,0,0.0,
                           "NORMAL","INFORMATIVO","NORMAL",[],audit)
        return Jornada(fecha, turno, [], None, None, 0,0,0,0,0,0,0,0.0,
                       "SIN_MARCACIONES","PENDIENTE","FALTA_INJUSTIFICADA",
                       ["SIN_MARCACIONES"],audit)

    entrada = entradas[0] if entradas else None
    salida = salidas[-1] if salidas else None
    if not entrada or not salida or salida.dt <= entrada.dt:
        return Jornada(fecha, turno, ps, entrada.dt if entrada else None,
                       salida.dt if salida else None,0,0,0,0,0,0,0,0.0,
                       "MARCACION_INCOMPLETA","PENDIENTE","FALTA_INJUSTIFICADA",
                       ["MARCACION_INCOMPLETA"],audit)

    audit.append(f"Primera entrada: {entrada.dt:%H:%M}")
    audit.append(f"Última salida: {salida.dt:%H:%M}")
    interiores=[p for p in ps if entrada.dt < p.dt < salida.dt]
    comida=0
    for i,p in enumerate(interiores):
        if "SALIDA" not in p.tipo:
            continue
        retorno=next((q for q in interiores[i+1:] if "ENTRADA" in q.tipo),None)
        if retorno:
            pausa=int((retorno.dt-p.dt).total_seconds()//60)
            if pausa>0:
                comida += pausa
                audit.append(f"Pausa comida: {p.dt:%H:%M}-{retorno.dt:%H:%M} ({pausa} min)")
    if comida == 0:
        comida = COMIDA_MIN
        audit.append("Sin par completo de comida: descuento estándar 30 min")

    nocturno="NOCTURN" in str(turno).upper()
    ini=time(22,0) if nocturno else time(7,0)
    fin=time(5,30) if nocturno else time(15,30)
    expected_in=datetime.combine(fecha,ini)
    expected_out=datetime.combine(fecha+timedelta(days=1 if nocturno else 0),fin)
    late=max(0,int((entrada.dt-expected_in).total_seconds()//60))
    late = late if late > TOLERANCIA_MIN else 0
    meal_late=max(0,comida-COMIDA_MIN)
    early=max(0,int((expected_out-salida.dt).total_seconds()//60))
    early_auto=early if TOLERANCIA_MIN < early <= 30 else 0
    early_pending=early if early > 30 else 0
    late_out=max(0,int((salida.dt-expected_out).total_seconds()//60))
    total=late+meal_late+early_auto
    gross=(salida.dt-entrada.dt).total_seconds()/60
    hours=round(max(0,gross-comida)/60,2)
    inc=[]; impact="INFORMATIVO"; consequence="NORMAL"; state="NORMAL"
    if early_pending:
        inc.append(f"SALIDA_TEMPRANA_{early_pending}_MIN")
        impact="PENDIENTE"; consequence="SALIDA_TEMPRANA"; state="PENDIENTE"
    if total > REVISION_RETRASO_MIN:
        if late: inc.append(f"RETRASO_ENTRADA_{late}_MIN")
        if meal_late: inc.append(f"RETRASO_COMIDA_{meal_late}_MIN")
        if early_auto: inc.append(f"SALIDA_TEMPRANA_AUTO_{early_auto}_MIN")
        inc.append(f"TOTAL_RETRASO_{total}_MIN")
        impact="PENDIENTE"; consequence=f"ATRASO_{total}_MIN"; state="PENDIENTE"
    elif total and impact != "PENDIENTE":
        state="AUTOMATICO"
        audit.append(f"Descuento automático total: {total} min")
    if late_out > 30:
        inc.append(f"SALIDA_TARDIA_{late_out}_MIN")
        if impact != "PENDIENTE":
            impact="INFORMATIVO"; consequence="NORMAL"; state="INFORMATIVO"
    return Jornada(fecha, turno, ps, entrada.dt, salida.dt, comida,late,meal_late,
                   early_auto,early_pending,late_out,total,hours,state,impact,
                   consequence,inc,audit)


def jornada_dict(j: Jornada) -> dict:
    d=asdict(j)
    d["fecha"]=j.fecha.isoformat()
    d["entrada"]=j.entrada.isoformat(sep=" ") if j.entrada else ""
    d["salida"]=j.salida.isoformat(sep=" ") if j.salida else ""
    d["punches"]=[{"dt":p.dt.isoformat(sep=" "),"tipo":p.tipo,"raw":p.raw} for p in j.punches]
    return d

