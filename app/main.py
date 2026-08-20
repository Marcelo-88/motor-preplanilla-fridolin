from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from app.processors.validar_datos import (
    separar_biometrico_no_identificado,
    validar_maestro,
)


def ejecutar_fase_1(
    archivo: Path,
    hoja_maestro: str = "01_MAESTRO_EMPLEADOS",
    hoja_biometrico: str = "02_BIOMETRICO_RAW",
    salida: Path | None = None,
) -> dict[str, int]:
    maestro = pd.read_excel(archivo, sheet_name=hoja_maestro, dtype={"CI": str})
    biometrico = pd.read_excel(archivo, sheet_name=hoja_biometrico, dtype={"CI": str})

    resultado = validar_maestro(maestro)
    vinculado, no_identificado = separar_biometrico_no_identificado(
        biometrico, resultado.maestro_valido
    )

    if salida is not None:
        with pd.ExcelWriter(salida, engine="openpyxl") as writer:
            resultado.maestro_valido.to_excel(writer, "PERSONAL_VALIDO", index=False)
            resultado.maestro_excluido.to_excel(writer, "MAESTRO_EXCLUIDO", index=False)
            resultado.advertencias.to_excel(writer, "ADVERTENCIAS", index=False)
            vinculado.to_excel(writer, "BIOMETRICO_VINCULADO", index=False)
            no_identificado.to_excel(writer, "NO_IDENTIFICADO", index=False)

    resumen = dict(resultado.resumen)
    resumen["biometrico_vinculado"] = len(vinculado)
    resumen["biometrico_no_identificado"] = len(no_identificado)
    return resumen


def main() -> None:
    parser = argparse.ArgumentParser(description="Motor PrePlanilla - Fase 1")
    parser.add_argument("archivo", type=Path, help="Archivo Excel de entrada")
    parser.add_argument("--salida", type=Path, default=Path("resultado_fase_1.xlsx"))
    args = parser.parse_args()

    resumen = ejecutar_fase_1(args.archivo, salida=args.salida)
    for clave, valor in resumen.items():
        print(f"{clave}: {valor}")


if __name__ == "__main__":
    main()
