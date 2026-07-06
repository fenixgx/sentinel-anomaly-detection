"""
🧭 MIGA DE PAN: Arquitectura de la red neuronal (MLP para detección de anomalías)
📍 UBICACIÓN: src/model.py

🎯 PORQUÉ EXISTE: Es EL requisito central de la prueba — "queremos ver cómo construyes
   la clase de la arquitectura de la red". Aquí se define la red densa (MLP) en PyTorch
   de forma explícita, sin usar el modelo de sklearn.
🚨 CUIDADO: La última capa devuelve UN logit SIN sigmoide. La sigmoide la aplica la
   función de pérdida (BCEWithLogitsLoss), que es numéricamente más estable que aplicar
   sigmoide + BCELoss por separado. Para predecir probabilidades, aplicar torch.sigmoid()
   a la salida (ver predict.py).
📋 SPEC: SPEC-001-sentinel — R2 (arquitectura de red) — CREATED
"""

from __future__ import annotations
import torch
import torch.nn as nn


class AnomalyMLP(nn.Module):
    """
    Perceptrón multicapa (red densa) para clasificación binaria: ¿fallo (1) o no (0)?

    Arquitectura:
        4 sensores  ->  Linear(32) -> ReLU -> Dropout
                     ->  Linear(16) -> ReLU -> Dropout
                     ->  Linear(1)   (un logit)

    Se eligió un MLP y NO un LSTM porque cada lectura de sensores se clasifica de forma
    independiente (datos tabulares), no como una secuencia temporal. Para esta señal, un
    MLP sobre features bien diseñadas rinde igual, es más interpretable y más fácil de
    mantener en producción. El LSTM tendría sentido si predijéramos el fallo a partir de
    la EVOLUCIÓN temporal de cada servidor (trabajo futuro).
    """

    def __init__(
        self,
        n_features: int,
        hidden1: int = 32,
        hidden2: int = 16,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        # nn.Sequential encadena las capas. Dropout apaga neuronas al azar durante el
        # entrenamiento -> regularización -> el modelo generaliza mejor (menos overfitting).
        self.net = nn.Sequential(
            nn.Linear(n_features, hidden1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden2, 1),  # 1 salida = logit crudo (la sigmoide va en la loss)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Paso hacia adelante.
        Entra un tensor (batch, n_features) y sale (batch,) con un logit por muestra.
        El .squeeze(-1) convierte la forma (batch, 1) en (batch,) para que encaje con las
        etiquetas, que son un vector 1D. Esto es gestión explícita de la forma del tensor.
        """
        logits = self.net(x)
        return logits.squeeze(-1)
