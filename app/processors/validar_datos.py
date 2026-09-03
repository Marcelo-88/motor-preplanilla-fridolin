from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable
import re

import pandas as pd


REQUIRED_MASTER_COLUMNS = {"CI", "Tipo_Personal"}
REQUIRED_BIOMETRIC_COLUMNS = {"CI"}


def normalizar_ci(value: object) -> str:
    """Normaliza el identificador sin asumir que sea estrictamente numérico."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return ""
    if re.fullmatch(r"\d+\.0", text):
        text = text[:-2]
    return re.sub(r"\s+", "", text).upper()


def _validate_columns(frame: pd.DataFrame, required: set[str], source: str) -> None:
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{source}: faltan columnas obligatorias: {sorted(missing)}")


@dataclass
class ResultadoValidacion:
    maestro_valido: pd.DataFrame
    maestro_excluido: pd.DataFrame
    advertencias: pd.DataFrame
    resumen: dict[str, int] = field(default_factory=dict)


def validar_maestro(maestro: pd.DataFrame) -> ResultadoValidacion:
    """Aplica las reglas de calidad acordadas para el maestro."""
    _validate_columns(maestro, REQUIRED_MASTER_COLUMNS, "MAESTRO")

    df = maestro.copy()
    df["CI_NORMALIZADO"] = df["CI"].map(normalizar_ci)
    if "Nombre_Completo" not in df.columns:
        df["Nombre_Completo"] = ""
    if "Supervisor" not in df.columns:
        df["Supervisor"] = ""
    if "Estado" not in df.columns:
        df["Estado"] = "Activo"
    estado = df["Estado"].fillna("Activo").astype(str).str.strip().str.upper()
    df["ESTADO_LABORAL"] = estado.map(
        lambda value: "RETIRADO" if "RETIR" in value else "ACTIVO"
    )

    sin_ci = df["CI_NORMALIZADO"].eq("")
    sin_tipo = df["Tipo_Personal"].fillna("").astype(str).str.strip().eq("")
    duplicado = df["CI_NORMALIZADO"].duplicated(keep=False) & ~sin_ci

    excluido = df[sin_ci | sin_tipo | duplicado].copy()
    excluido["ESTADO_PROCESAMIENTO"] = "EXCLUIDO"
    excluido["MOTIVO_EXCLUSION"] = ""
    excluido.loc[sin_ci, "MOTIVO_EXCLUSION"] = "SIN_CI"
    excluido.loc[~sin_ci & sin_tipo, "MOTIVO_EXCLUSION"] = "SIN_TIPO_PERSONAL"
    excluido.loc[~sin_ci & ~sin_tipo & duplicado, "MOTIVO_EXCLUSION"] = "CI_DUPLICADO"

    valido = df[~(sin_ci | sin_tipo | duplicado)].copy()
    valido["ESTADO_PROCESAMIENTO"] = "VALIDO"

    advertencias = valido[valido["Supervisor"].fillna("").astype(str).str.strip().eq("")].copy()
    advertencias = advertencias[["CI", "CI_NORMALIZADO", "Nombre_Completo"]]
    advertencias["TIPO"] = "SIN_SUPERVISOR"
    advertencias["SEVERIDAD"] = "ADVERTENCIA"
    advertencias["BLOQUEA_ANALISIS"] = False

    return ResultadoValidacion(
        maestro_valido=valido,
        maestro_excluido=excluido,
        advertencias=advertencias,
        resumen={
            "maestro_total": len(df),
            "maestro_valido": len(valido),
            "maestro_excluido": len(excluido),
            "sin_supervisor": len(advertencias),
            "personal_activo": int(valido["ESTADO_LABORAL"].eq("ACTIVO").sum()),
            "personal_retirado": int(valido["ESTADO_LABORAL"].eq("RETIRADO").sum()),
        },
    )


def separar_biometrico_no_identificado(
    biometrico: pd.DataFrame,
    maestro_valido: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve biométrico vinculado y registros cuyo CI no existe en el maestro válido."""
    _validate_columns(biometrico, REQUIRED_BIOMETRIC_COLUMNS, "BIOMETRICO")
    bio = biometrico.copy()
    bio["CI_NORMALIZADO"] = bio["CI"].map(normalizar_ci)
    valid_ids = set(maestro_valido["CI_NORMALIZADO"])
    mask = bio["CI_NORMALIZADO"].isin(valid_ids)

    vinculado = bio[mask].copy()
    no_identificado = bio[~mask].copy()
    no_identificado["ESTADO"] = "PENDIENTE"
    no_identificado["MOTIVO"] = "CI_NO_EXISTE_EN_MAESTRO_VALIDO"
    return vinculado, no_identificado
