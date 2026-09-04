# Formato de preplanilla por supervisor — versión 1

Estado: validado con las preplanillas de Medrano y Cabrera; tratamiento nocturno en validación con Flores, agosto de 2026.

## Alcance

Esta versión define el formato base de los documentos que revisan los supervisores. Todavía no incluye bolsa de horas extra ni planilla final de Recursos Humanos.\n\n## Cambios de turno dentro del mes

El maestro conserva la asignación final del empleado y tres campos para reconstruir su historial mensual:

- `Turno Completo`: `S` cuando mantuvo un único turno durante todo el periodo; `N` cuando cambió de turno.
- `Fecha DIurno`: rango o rangos en los que corresponde aplicar el horario diurno.
- `Fecha Nocturno`: rango o rangos en los que corresponde aplicar el horario nocturno.

Reglas del motor:

- Con `Turno Completo = S`, se utiliza normalmente el turno, área y supervisor registrados al cierre del mes.
- Con `Turno Completo = N`, cada jornada se reconstruye usando el turno correspondiente a su fecha.
- Las fechas nocturnas usan 22:00–05:30 del día siguiente; las diurnas usan 07:00–15:30.
- Una fecha que no pertenece a ninguno de los rangos no recibe un turno supuesto y no genera una falta automática.
- El empleado se excluye de las pestañas generales para evitar duplicación.
- Sus excepciones reales se presentan en `CAMBIOS_DE_TURNO` dentro de la preplanilla del supervisor final registrado en el maestro.

### Caso de validación: Silvia Chambi

- CI: `6754961`.
- Nombre: Chambi Vasquez Silvia Antonia.
- Asignación final: turno diurno, Panadería y Repostería, supervisora Navarro Isabel.
- `Turno Completo = N`.
- Nocturno: 01/08/2026–08/08/2026.
- Diurno: 10/08/2026–31/08/2026.
- El 09/08/2026 queda fuera de ambos rangos y no debe producir ausencia automática.
- Ya fue eliminada completamente de la preplanilla de Flores, incluida la auditoría.
- Pendiente: recalcular sus jornadas con ambos horarios y generar únicamente sus excepciones en `CAMBIOS_DE_TURNO` de la preplanilla de Navarro.

## Personal retirado

- El estado laboral se toma de la pestaña `01_Maestro_Empleados`.
- El personal retirado nunca aparece en `01_FIJOS_EVENTUALES` ni en `02_JORNALEROS`.
- Si tuvo marcaciones dentro del periodo, sus excepciones se presentan en `03_PERSONAL_RETIRADO` para validación.
- Si no tuvo ninguna actividad biométrica durante el mes, no se le generan faltas ficticias.
- Cuando exista fecha de retiro, el motor debe evaluar únicamente desde el inicio del periodo hasta su último día laboral.

## Personal jornalero\n\n- La pestaña de jornaleros presenta solamente excepciones que requieren decisión; no muestra días trabajados normalmente.\n- Una jornada completa normal equivale a `1_TURNO` y no se incluye en el documento de revisión.\n- Un día sin marcaciones o con una marcación incompleta queda `PENDIENTE` y parte de `0_TURNOS` hasta que el supervisor confirme que fue trabajado.\n- Los retrasos se conservan como información de conducta, pero no reducen el jornal: el pago se determina por día trabajado.\n- Una jornada que supera 9 horas netas se propone como `TURNO_Y_MEDIO_POR_VALIDAR`.\n- El turno y medio nunca se concede automáticamente. Mientras está pendiente conserva `1_TURNO`; únicamente `APROBAR_TURNO_Y_MEDIO` cambia el pago a `1.5_TURNOS`.\n- En nocturno, la fecha operativa corresponde a la noche de entrada y la salida se busca en la mañana siguiente dentro de la ventana de esa jornada.\n- Para nocturnos se excluye el sábado como día de inicio regular; para diurnos se excluye el domingo.\n- Las tarifas generales y las excepciones de tarifa por persona se mantienen en `06_Tarifas_Jornaleros` del documento matriz.

## Identificación del empleado

- Cada persona debe existir una sola vez en `01_Maestro_Empleados`.
- `Carnet_Identidad` es el identificador oficial.
- `ID_Biometrico` conserva el identificador usado por el biométrico.
- El motor debe vincular marcaciones por cualquiera de los dos identificadores y consolidarlas bajo el CI oficial.
- Ever Medrano se excluye de los documentos de revisión y de la planilla final.

## Reglas horarias validadas

- Diurno: 07:00 a 15:30.
- Nocturno: 22:00 a 05:30 del día siguiente.
- Se usa la primera entrada y la última salida dentro de la ventana de jornada.
- Si existen varias entradas o salidas, se conserva la primera entrada y la última salida como límites de jornada.
- La comida o cena tiene 30 minutos.
- Si no existe un par completo de comida, se descuenta el estándar de 30 minutos, pero no se genera incidencia solo por esa omisión.
- El exceso de comida se suma al retraso de entrada.
- Una salida temprana de hasta 10 minutos está dentro de tolerancia.
- Una salida temprana entre 11 y 30 minutos se suma al retraso total.
- Una salida más de 30 minutos antes es una excepción pendiente de aprobación.
- Una salida más de 30 minutos después es informativa; sin aprobación no acredita horas extra ni genera sanción.
- Un retraso total de hasta 60 minutos se procesa automáticamente.
- Un retraso total superior a 60 minutos requiere revisión.
- Sin marcaciones o con jornada incompleta, la consecuencia sin respuesta es falta injustificada.
- Una incidencia informativa sin decisión se procesa como normal.
- Una incidencia pendiente sin decisión aplica su consecuencia base.

## Personal STAFF

- STAFF se identifica por `Area_Departamento = Staff`.
- No se controlan retrasos, pausas, salidas tempranas ni horas extra.
- Cualquier marcación biométrica confirma presencia.
- Solo aparecen como excepción los días laborables sin ninguna marcación.
- Esos días deben aprobarse o rechazarse por permiso, vacación u otra justificación.

## Orden de columnas

1. CI
2. Nombre
3. Fecha
4. Día
5. Excepción consolidada
6. Impacto
7. Decisión supervisor
8. Consecuencia
9. Observación supervisor
10. Columna separadora en blanco, blanca y sin bordes
11. Turno
12. Área
13. Marcaciones RAW
14. Jornada reconstruida
15. Horas trabajadas
16. Retraso entrada
17. Retraso comida
18. Salida temprana automática
19. Total retraso
20. Estado
21. Consecuencia base
22. Reglas aplicadas, únicamente en auditoría

## Campos editables y cálculos

- `Decisión supervisor` utiliza una lista cerrada de opciones.
- `Observación supervisor` es de texto libre.
- `Retraso entrada`, `Retraso comida` y `Salida temprana automática` son editables y se resaltan en amarillo.
- `Total retraso` es una fórmula: retraso de entrada + retraso de comida + salida temprana automática.
- La excepción consolidada conserva la detección original del motor como evidencia.
- La consecuencia se recalcula usando la decisión y el total corregido.

## Consecuencia según decisión

- Sin decisión o `PENDIENTE`: conserva la consecuencia base, ajustando los minutos si se corrigió el retraso.
- `JUSTIFICAR_FALTA`: `FALTA_JUSTIFICADA`.
- `APROBADO_HE`: `HE_APROBADA`.
- `APROBAR_TURNO_Y_MEDIO`: `TURNO_Y_MEDIO_APROBADO`.
- `APROBADO` o `VALIDAR_TRABAJADO`: `NORMAL`.
- `RECHAZADO`: conserva la consecuencia base, ajustada al total corregido.

## Estructura del archivo

- `00_INSTRUCCIONES`
- `01_FIJOS_EVENTUALES`
- `02_JORNALEROS`
- `03_PERSONAL_RETIRADO`, cuando existan retirados asignados al supervisor\n- `04_AUDITORIA` cuando exista la pestaña de retirados; en caso contrario `03_AUDITORIA`

Las secciones principal y técnica deben conservar filtros. Se congelan la fila de encabezados y las primeras cuatro columnas para facilitar la revisión.

