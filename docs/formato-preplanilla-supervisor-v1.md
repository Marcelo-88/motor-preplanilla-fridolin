# Formato de preplanilla por supervisor — versión 1

Estado: validado con la preplanilla de Medrano Fiorilo Ever Marcelo, agosto de 2026.

## Alcance

Esta versión define el formato base de los documentos que revisan los supervisores. Todavía no incluye bolsa de horas extra, consolidación de jornaleros ni planilla final de Recursos Humanos.

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
- `03_AUDITORIA`

Las secciones principal y técnica deben conservar filtros. Se congelan la fila de encabezados y las primeras cuatro columnas para facilitar la revisión.

