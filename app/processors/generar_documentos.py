from __future__ import annotations

from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

DECISIONES = "PENDIENTE,APROBADO,APROBADO_HE,JUSTIFICAR_FALTA,VALIDAR_TRABAJADO,APROBAR_TURNO_Y_MEDIO,RECHAZADO"
ESTADOS = "PENDIENTE,REVISADO,CONCLUIDO"
COLUMNAS = [
    "Estado", "Empleado", "CI", "Fecha operativa", "Día", "Turno", "Área",
    "Marcaciones", "Pares", "Horas trabajadas", "Excepción consolidada",
    "Impacto", "Consecuencia sin acción", "Decisión supervisor",
    "Observación supervisor",
]


def _crear_pestana(ws, filas: list[dict], nombre_tabla: str) -> None:
    ws.append(COLUMNAS)
    for fila in filas:
        ws.append([fila.get(c, "") for c in COLUMNAS])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:O{max(2, ws.max_row)}"
    for cell in ws[1]:
        cell.fill = PatternFill("solid", fgColor="E8EAED")
        cell.font = Font(bold=True)
    if ws.max_row >= 2:
        tabla = Table(displayName=nombre_tabla, ref=f"A1:O{ws.max_row}")
        tabla.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False
        )
        ws.add_table(tabla)
    dv_estado = DataValidation(type="list", formula1=f'"{ESTADOS}"')
    dv_decision = DataValidation(type="list", formula1=f'"{DECISIONES}"')
    ws.add_data_validation(dv_estado)
    ws.add_data_validation(dv_decision)
    dv_estado.add(f"A2:A{max(2, ws.max_row)}")
    dv_decision.add(f"N2:N{max(2, ws.max_row)}")
    anchos = [14, 30, 14, 16, 13, 12, 20, 42, 28, 16, 38, 16, 25, 25, 38]
    for i, ancho in enumerate(anchos, 1):
        ws.column_dimensions[chr(64 + i)].width = ancho


def generar_documentos_supervisor(
    incidencias: pd.DataFrame, salida: Path
) -> list[Path]:
    salida.mkdir(parents=True, exist_ok=True)
    obligatorias = {"Supervisor_Asignado", "Tipo_Personal", *COLUMNAS}
    faltantes = obligatorias - set(incidencias.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {sorted(faltantes)}")
    archivos = []
    for supervisor, grupo in incidencias.groupby("Supervisor_Asignado", dropna=False):
        supervisor = str(supervisor or "SIN SUPERVISOR ASIGNADO").strip()
        wb = Workbook()
        wb.remove(wb.active)
        instrucciones = wb.create_sheet("00_INSTRUCCIONES")
        instrucciones.append(["REVISIÓN DE EXCEPCIONES — PREPLANILLA FRIDOLIN"])
        instrucciones.append(["Supervisor", supervisor])
        instrucciones.append(["Regla", "INFORMATIVO sin acción = NORMAL"])
        instrucciones.append(["Regla", "PENDIENTE sin acción = aplicar consecuencia"])
        fijos = grupo[~grupo["Tipo_Personal"].astype(str).str.contains("Jornal", case=False, na=False)]
        jorn = grupo[grupo["Tipo_Personal"].astype(str).str.contains("Jornal", case=False, na=False)]
        _crear_pestana(wb.create_sheet("01_FIJOS_EVENTUALES"), fijos.to_dict("records"), "FijosEventuales")
        _crear_pestana(wb.create_sheet("02_JORNALEROS"), jorn.to_dict("records"), "Jornaleros")
        wb.create_sheet("03_AUDITORIA")
        nombre = "".join(ch if ch.isalnum() else "_" for ch in supervisor).strip("_")
        destino = salida / f"Revision_PrePlanilla_{nombre}.xlsx"
        wb.save(destino)
        archivos.append(destino)
    return archivos
