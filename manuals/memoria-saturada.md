# Memoria saturada

## Síntomas
- Uso de memoria RAM por encima del 85 %.
- Riesgo de swapping (uso de disco como memoria) y de que el OOM killer termine procesos.

## Causa probable
La demanda de memoria supera la disponible. Causas frecuentes: fugas de memoria en
aplicaciones, procesos mal dimensionados, cachés sin límite, o crecimiento de la carga sin
escalar. El swapping degrada gravemente el rendimiento y puede acabar en la caída del servicio.

## Acciones recomendadas
1. Identificar los procesos con mayor consumo de memoria.
2. Reiniciar los servicios con fugas de memoria conocidas.
3. Revisar y ajustar los límites de memoria de contenedores y servicios.
4. Añadir memoria física o escalar horizontalmente si la carga es legítima.
5. Configurar alertas que avisen antes de llegar al 90 % de uso.
