# Historial de implementación — agosto 2026

Última actualización: 4 de septiembre de 2026.

## Objetivo vigente

Generar preplanillas por supervisor en Drive, usando el repositorio `motor-preplanilla-fridolin` para leer el biométrico, aplicar las reglas del repositorio base `preplanilla-fridolin` y presentar solamente excepciones que requieren revisión. La bolsa de horas extra, la lectura final de decisiones y la planilla consolidada de Recursos Humanos permanecen pendientes.

## Decisiones consolidadas

1. El repositorio de la aplicación original no se modifica; funciona como modelo de reglas.
2. El desarrollo se realiza en el motor nuevo.
3. El mes piloto es agosto de 2026 completo.
4. Los documentos se generan por supervisor y se almacenan en Drive.
5. Los días normales no deben saturar las pestañas de revisión.
6. Las incidencias informativas sin decisión continúan como normales.
7. Las incidencias pendientes sin decisión aplican su consecuencia base.
8. Los minutos de retraso pueden corregirse manualmente y las fórmulas recalculan total y consecuencia.
9. Los casos de personal retirado y cambios de turno se aíslan en pestañas separadas.
10. La habilidad reutilizable se creará solamente después de que el usuario apruebe todas las preplanillas.

## Documentos trabajados

- Medrano: formato principal validado; STAFF sin control de retrasos u horas extra; Ever Medrano excluido.
- Cabrera: formato actualizado y jornaleros reducidos a excepciones.
- Flores: formato nocturno actualizado; Silvia Chambi retirada del documento porque terminó el mes bajo Navarro.
- Navarro: formato actualizado; Silvia Chambi aparece solamente en `03_CAMBIOS_DE_TURNO`.
- Cruz Olmos: todavía requiere revisión con el formato final consolidado.

## Actualización del 4 de septiembre de 2026

Por instrucción del usuario se reconstruyeron y reemplazaron en Drive únicamente Medrano, Cabrera y Flores. Cruz Olmos y Navarro no fueron modificadas.

- Medrano: 49 excepciones de fijos/eventuales, 0 jornaleros y 133 registros de auditoría.
- Cabrera: 251 excepciones de fijos/eventuales, 8 excepciones de jornaleros y 620 registros de auditoría.
- Flores: 171 excepciones de fijos/eventuales, 87 excepciones de jornaleros, 0 retirados con actividad y 372 registros de auditoría.
- Los tres documentos quedaron sin errores de fórmula.
- Silvia Chambi no aparece en ninguno de estos tres documentos; su tratamiento permanece aislado en Navarro.

## Resultado actual de Navarro

- `01_FIJOS_EVENTUALES`: 142 filas de excepción.
- `02_JORNALEROS`: 51 filas de excepción correspondientes a 3 personas; 48 sin marcaciones y 3 con jornada incompleta.
- `03_CAMBIOS_DE_TURNO`: 13 filas de Silvia Chambi; 10 pendientes y 3 informativas.
- `04_PERSONAL_RETIRADO`: sin casos con actividad vinculada.
- `05_AUDITORIA`: 372 registros técnicos.
- Validación: sin errores de fórmula.

## Caso Silvia Chambi

- Maestro final: turno diurno y supervisora Navarro Isabel.
- Rango nocturno: 01/08 al 08/08.
- Rango diurno: 10/08 al 31/08.
- El 09/08 no pertenece a ninguno de los rangos.
- Las marcaciones atípicas del rango nocturno se conservan como evidencia.
- Todo lo raro se presenta en `CAMBIOS_DE_TURNO`; el supervisor final decide.

## Pendientes antes de crear la habilidad

- Revisar y aprobar Flores.
- Revisar y aprobar Navarro.
- Aplicar y revisar el formato final en Cruz Olmos.
- Confirmar que no quedan ajustes en Medrano y Cabrera.
- Definir la capacitación de supervisores.
- Crear la habilidad que genere y actualice las preplanillas con estas reglas.
- Posteriormente crear la habilidad que lea decisiones y prepare la planilla para Recursos Humanos.

