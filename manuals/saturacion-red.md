# Saturación de red

## Síntomas
- Tráfico de red por encima de 700 Mbps de forma sostenida.
- Latencia elevada y pérdida de paquetes.

## Causa probable
El ancho de banda disponible se agota. Causas frecuentes: picos de tráfico legítimo,
transferencias masivas de datos, ataques de denegación de servicio (DDoS), o una
configuración de red subóptima. La saturación degrada todos los servicios que dependen
de la red.

## Acciones recomendadas
1. Identificar el origen del tráfico (IPs, servicios, transferencias en curso).
2. Descartar tráfico anómalo o un posible ataque revisando los patrones.
3. Aplicar QoS o limitar las transferencias no críticas.
4. Escalar el ancho de banda o balancear la carga hacia otros nodos.
5. Revisar la configuración de red y los límites de las interfaces.
