import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from sustentacao import TeoriaLinhaSustentação, TeoriaLinhaSustentacaoFormacao


class VisualizacaoFormacao:
    def __init__(self, diretorio_saida="saida"):
        """
        Classe para encapsular os cálculos e a visualização do impacto da formação em voo.
        :param diretorio_saida: Diretório onde os gráficos serão salvos. Default é "saida".
        """
        self.dados_resultados = {
            "Razão de Aspecto": [],
            "Ângulo Induzido (graus)": [],
            "Tipo": [],
            "Razão (Formação/Solo)": [],
        }
        self.diretorio_saida = diretorio_saida
        if not os.path.exists(diretorio_saida):
            os.makedirs(diretorio_saida)

    def calcular_resultados(self, razoes_aspecto, angulos_induzidos, angulo_ataque, angulos_estacoes, termos_considerados, distancias, distribuicao_corda, angulo_sustentacao_nula):
        """
        Calcula os coeficientes normalizados para diferentes razões de aspecto e ângulos induzidos.
        """
        for angulo_induzido in angulos_induzidos:
            for razao_aspecto in razoes_aspecto:
                # Instância da classe
                formacao_prandtl = TeoriaLinhaSustentacaoFormacao(num_aeronaves=3, c_d0=0.02)
                formacao_prandtl.carregar_parametros_geometricos(
                    razao_aspecto=razao_aspecto,
                    razao_afilamento=1.0,
                    area=10.0,
                    distribuicao_corda=distribuicao_corda,
                    angulo_sustentacao_nula=angulo_sustentacao_nula,
                )

                # Resolvendo para a formação
                formacao_prandtl.resolver_formacao(
                    angulo_ataque=angulo_ataque + angulo_induzido,
                    angulos_estacoes=angulos_estacoes,
                    termos_considerados=termos_considerados,
                    distancias=distancias,
                )

                # Coeficientes da aeronave líder (voo solo)
                cl_solo = formacao_prandtl.coeficientes_sustentacao_formacao[0]
                cd_solo = formacao_prandtl.coeficientes_arrasto_total[0]
                cdi_solo = formacao_prandtl.coeficientes_arrasto_induzido[0]

                # Coeficientes da formação (aeronave 2 como referência)
                cl_formacao = formacao_prandtl.coeficientes_sustentacao_formacao[1]
                cd_formacao = formacao_prandtl.coeficientes_arrasto_total[1]
                cdi_formacao = formacao_prandtl.coeficientes_arrasto_induzido[1]

                # Razões normalizadas
                self.dados_resultados["Razão de Aspecto"].extend([razao_aspecto, razao_aspecto, razao_aspecto])
                self.dados_resultados["Ângulo Induzido (graus)"].extend([np.degrees(angulo_induzido)] * 3)
                self.dados_resultados["Tipo"].extend(["CL", "CD", "CDi"])
                self.dados_resultados["Razão (Formação/Solo)"].extend([
                    cl_formacao / cl_solo,
                    cd_formacao / cd_solo,
                    cdi_formacao / cdi_solo,
                ])

    def plotar_e_salvar(self):
        """
        Cria os gráficos para diferentes ângulos induzidos e salva no diretório de saída.
        """
        resultados_df = pd.DataFrame(self.dados_resultados)
        sns.set(style="whitegrid")
        nomes_arquivos = {
            2: "angulo_induzido_2.jpeg",
            4: "angulo_induzido_4.jpeg",
            6: "angulo_induzido_6.jpeg",
            8: "angulo_induzido_8.jpeg",
        }

        for angulo_induzido_graus in resultados_df["Ângulo Induzido (graus)"].unique():
            subconjunto = resultados_df[resultados_df["Ângulo Induzido (graus)"] == angulo_induzido_graus]
            plt.figure(figsize=(10, 6))
            sns.lineplot(
                data=subconjunto,
                x="Razão de Aspecto",
                y="Razão (Formação/Solo)",
                hue="Tipo",
                marker="o",
            )
            plt.title(f"Razão CL, CD, CDi (Formação/Solo) vs Razão de Aspecto\nÂngulo Induzido: {angulo_induzido_graus}°")
            plt.xlabel("Razão de Aspecto")
            plt.ylabel("Razão (Formação/Solo)")
            plt.legend(title="Tipo de Coeficiente")
            plt.grid(True)

            arquivo_saida = os.path.join(self.diretorio_saida, nomes_arquivos[int(angulo_induzido_graus)])
            plt.savefig(arquivo_saida, format="jpeg", dpi=300)
            plt.close()

        print(f"Gráficos salvos no diretório: {self.diretorio_saida}")
