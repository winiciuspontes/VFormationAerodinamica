import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sustentacao import TeoriaLinhaSustentação, TeoriaLinhaSustentacaoFormacao
from grafico import VisualizacaoFormacao


if __name__ == "__main__":
    # Parâmetros de exemplo para executar
    aspect_ratios = np.linspace(5, 20, 10)  # Razão de aspecto variando de 5 a 20
    induced_angles = np.radians([2, 4, 6, 8])  # Ângulos de ataque induzido em radianos

    # Demais parâmetros (substitua pelos valores adequados no seu contexto)
    angle_of_attack = np.radians(5)  # Ângulo de ataque base
    station_angles = np.linspace(0.1, np.pi - 0.1, 10)  # Ângulos das estações
    considered_terms = list(range(1, 11))  # Termos da série de Fourier
    distances = [2.0, 2.0]  # Distâncias longitudinais entre aeronaves
    c0 = 1.0  # Corda na raiz
    chord_distribution = lambda theta: c0 * np.sin(theta)
    zero_lift_angle = lambda theta: 0.0  # Ângulo constante

    # Instanciando a classe e gerando os resultados e gráficos
    visualization = VisualizacaoFormacao(diretorio_saida="output")
    visualization.calcular_resultados(aspect_ratios, induced_angles, angle_of_attack, station_angles, considered_terms, distances, chord_distribution, zero_lift_angle)
    visualization.plotar_e_salvar()