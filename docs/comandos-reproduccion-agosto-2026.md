# Comandos de reproducción — agosto 2026

Estos comandos documentan la secuencia actual. Deben ejecutarse desde la raíz del proyecto y usando las versiones vigentes de los archivos del maestro y del biométrico.

## Procesamiento base

```powershell
python engine_workspace/process_august.py
python engine_workspace/test_preplanilla_engine.py
```

## Construcción inicial de documentos

```powershell
node outputs/engine_agosto_2026/build_documents.mjs
```

## Preparación del maestro

```powershell
node outputs/engine_agosto_2026/edit_employee_matrix.mjs
node outputs/engine_agosto_2026/mark_retired_employees.mjs
node outputs/engine_agosto_2026/add_jornalero_rates.mjs
```

## Reconstrucción del caso con cambio de turno

```powershell
python outputs/engine_agosto_2026/build_silvia_shift_rows.py
```

## Generación por supervisor con el formato final

```powershell
node outputs/engine_agosto_2026/edit_medrano_staff.mjs "Medrano Fiorilo Ever Marcelo" "Revision_PrePlanilla_MEDRANO_FIORILO_EVER_MARCELO_Agosto_2026.xlsx"
node outputs/engine_agosto_2026/edit_medrano_staff.mjs "CABRERA AGUILERA YASMIN" "Revision_PrePlanilla_CABRERA_AGUILERA_YASMIN_Agosto_2026.xlsx"
node outputs/engine_agosto_2026/edit_medrano_staff.mjs "Flores Andrea Natalia" "Revision_PrePlanilla_FLORES_ANDREA_NATALIA_Agosto_2026.xlsx"
node outputs/engine_agosto_2026/edit_medrano_staff.mjs "NAVARRO ISABEL" "Revision_PrePlanilla_NAVARRO_ISABEL_Agosto_2026.xlsx"
node outputs/engine_agosto_2026/edit_medrano_staff.mjs "CRUZ OLMOS JULIA" "Revision_PrePlanilla_CRUZ_OLMOS_JULIA_Agosto_2026.xlsx"
```

## Orden obligatorio para una ejecución futura

1. Leer el maestro y el control de vinculación.
2. Consolidar CI, PIN e ID biométrico.
3. Aplicar estado laboral y rangos de turno.
4. Procesar todas las marcaciones.
5. Reconstruir jornadas diurnas y nocturnas.
6. Calcular excepciones y consecuencias.
7. Separar fijos, jornaleros, cambios de turno y retirados.
8. Generar un archivo por supervisor.
9. Validar fórmulas, filtros, listas y formato visual.
10. Reemplazar el archivo correspondiente en Drive conservando su ID.

No debe crearse la planilla final de Recursos Humanos ni la bolsa de horas extra durante esta etapa.

