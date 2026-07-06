# CPU saturada

## Síntomas
- Uso de CPU sostenido por encima del 85 %.
- Tiempos de respuesta degradados y colas de trabajo que crecen.

## Causa probable
La carga de trabajo supera la capacidad de cómputo del servidor. Causas habituales: picos de
tráfico, procesos en bucle, consultas o algoritmos ineficientes, o falta de escalado. La
saturación sostenida de CPU, combinada con calor, acelera el desgaste y puede provocar caídas.

## Acciones recomendadas
1. Identificar los procesos que más CPU consumen.
2. Revisar procesos en bucle o consultas ineficientes que disparen el uso.
3. Escalar horizontalmente (añadir nodos) o verticalmente si el pico es puntual.
4. Aplicar límites de CPU a los procesos no críticos.
5. Vigilar la temperatura: CPU alta junto con calor alto es riesgo de sobrecarga térmica.
