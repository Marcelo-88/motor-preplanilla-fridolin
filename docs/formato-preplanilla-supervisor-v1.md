# Formato de preplanilla por supervisor — versión 1

Estado: formato aplicado a Medrano, Cabrera, Flores y Navarro. El tratamiento nocturno y los cambios de turno continúan sujetos a validación funcional del usuario antes de convertir el proceso en una habilidad.

## Alcance

Esta versión define el formato base de los documentos que revisan los supervisores. Todavía no incluye bolsa de horas extra ni planilla final de Recursos Humanos.

## Personal jornalero

- La pestaña de jornaleros presenta solamente excepciones que requieren decisión; no muestra días trabajados normalmente.
- Una jornada completa normal equivale a `1_TURNO` y no se incluye en el documento de revisión.
- Un día sin marcaciones o con una marcación incompleta queda `PENDIENTE` y parte de `0_TURNOS` hasta que el supervisor confirme que fue trabajado.
- Los retrasos se conservan como información de conducta, pero no reducen el jornal: el pago se determina por día trabajado.
- Una jornada que supera 9 horas netas se propone como `TURNO_Y_MEDIO_POR_VALIDAR`.
- El turno y medio nunca se concede automáticamente. Mientras está pendiente conserva `1_TURNO`; únicamente `APROBAR_TURNO_Y_MEDIO` cambia el pago a `1.5_TURNOS`.
- En nocturno, la fecha operativa corresponde a la noche de entrada y la salida se busca en la mañana siguiente dentro de la ventana de esa jornada.
- Para nocturnos se excluye el sábado como día de inicio regular; para diurnos se excluye el domingo.
- Las tarifas generales y las excepciones de tarifa por persona se mantienen en `06_Tarifas_Jornaleros` del documento matriz.

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

## Personal retirado

- El estado laboral se cruza con `Control Vinculación Personal Agosto 2026` y se conserva en el maestro.
- Una persona retirada que tuvo actividad durante una parte del mes aparece únicamente en `PERSONAL_RETIRADO`.
- No se generan faltas artificiales fuera de su periodo real de actividad.
- El personal retirado no se mezcla con la pestaña general.

## Cambios de turno o supervisor

- `Turno Completo = S` indica que el turno habitual aplica durante todo el mes.
- `Turno Completo = N` obliga al motor a leer los rangos `Fecha Diurno` y `Fecha Nocturno`.
- Cada fecha utiliza su horario correspondiente; las fechas fuera de ambos rangos no generan automáticamente una falta.
- La persona se asigna al supervisor final registrado en el maestro.
- Todas las situaciones atípicas de estas personas se aíslan en `CAMBIOS_DE_TURNO` y no aparecen en la pestaña general.
- El supervisor final decide qué hacer con cada excepción. El motor no corrige automáticamente una marcación rara.
- Caso piloto: Silvia Chambi, nocturno del 01/08 al 08/08 y diurno del 10/08 al 31/08. El 09/08 queda fuera de ambos rangos.

## Orden de columnas

1. CI
2. Nombre
3. Fecha
4. Día
5. Excepción consolidada
6. Impacto
7. Decisión supervisor
8. Consecuencia
9. Turnos a pagar, únicamente en jornaleros
10. Observación supervisor
11. Columna separadora en blanco, blanca y sin bordes
12. Turno
13. Área
14. Marcaciones RAW
15. Jornada reconstruida
16. Horas trabajadas
17. Retraso entrada
18. Retraso comida
19. Salida temprana automática
20. Total retraso
21. Estado
22. Consecuencia base
23. Reglas aplicadas, únicamente en auditoría

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

- `01_FIJOS_EVENTUALES`
- `02_JORNALEROS`
- `03_CAMBIOS_DE_TURNO`, cuando existen casos
- `PERSONAL_RETIRADO`, numerada según las pestañas anteriores
- `AUDITORIA`, como última pestaña y numerada según las pestañas anteriores

La pestaña de instrucciones fue eliminada de las preplanillas de supervisores.

Las secciones principal y técnica deben conservar filtros. Se congelan la fila de encabezados y las primeras cuatro columnas para facilitar la revisión.

