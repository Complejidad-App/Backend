import numpy as np

from app.schemas.analysis import HistogramBin, StatsResponse


def compute_stats(values: list[float], bins: int = 10) -> StatsResponse:
    """Calcula estadisticas descriptivas y un histograma a partir de una lista de numeros.

    Esta funcion es un ejemplo del tipo de "algoritmo" cuyo resultado se devuelve
    en JSON para que el frontend lo muestre graficamente. Sustituye o agrega aqui
    los algoritmos reales de tu analisis del dataset.
    """
    array = np.asarray(values, dtype=float)

    bin_count = min(bins, max(1, array.size))
    frequencies, edges = np.histogram(array, bins=bin_count)

    histogram = [
        HistogramBin(
            bin_start=float(edges[i]),
            bin_end=float(edges[i + 1]),
            frequency=int(frequencies[i]),
        )
        for i in range(len(frequencies))
    ]

    return StatsResponse(
        count=int(array.size),
        mean=float(np.mean(array)),
        median=float(np.median(array)),
        std=float(np.std(array)),
        min=float(np.min(array)),
        max=float(np.max(array)),
        histogram=histogram,
    )
