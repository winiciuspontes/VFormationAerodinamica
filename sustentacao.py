import numpy as np
import sympy as sp

class TeoriaLinhaSustentação(object):
    def __init__(self):
        """
        Classe que implementa todos os métodos necessários para obter dados da asa usando a Teoria da Linha de Sustentação de Prandtl. 
        Para resolver o sistema, o usuário deve especificar as estações nas quais a equação deve ser avaliada e os termos a serem considerados 
        na série de Fourier envolvida. Os passos para a solução são:
        1. Inicialize esta classe. Nenhuma entrada é necessária.
        2. Carregue todas as propriedades geométricas da asa: razão de aspecto, razão de afilamento, área superficial, distribuição de corda e
        ângulo de sustentação nula. A distribuição da corda deve ser uma função única de theta. O ângulo de sustentação nula pode ser
        uma constante ou uma função de theta. Ambos devem estar em radianos.
        3. Chame o método resolver desta classe para obter os coeficientes de Fourier desejados. Os coeficientes a serem avaliados são os 
        introduzidos pelo usuário em termos_considerados. Outras entradas são angulo_ataque, que pode ser uma constante ou uma função de 
        theta (em radianos), e os ângulos das estações.
        4. Uma vez conhecidos os coeficientes, os demais parâmetros podem ser facilmente avaliados.
        """
        self.razao_aspecto = None
        self.area = None
        self.razao_afilamento = None
        self.distribuicao_corda = None
        self.angulo_sustentacao_nula = None
        self.envergadura = None  # Envergadura da asa.
        self.termos_considerados = None  # Termos considerados da série de Fourier.
        self.angulos_estacoes = None  # Ângulos das estações usados para definir o sistema a ser resolvido.
        self.sistema = None  # Array contendo o sistema a ser resolvido.
        self.angulo_ataque = None
        self.simbolos = None
        self.coeficientes_fourier = dict()

    def carregar_parametros_geometricos(self, razao_aspecto, razao_afilamento, area, distribuicao_corda, angulo_sustentacao_nula):
        """
        Carregar parâmetros geométricos e calcular alguns outros parâmetros úteis.
        :param razao_aspecto: Razão de aspecto de toda a asa.
        :param razao_afilamento: Razão entre as cordas de ponta e raiz.
        :param area: Área da asa inteira.
        :param distribuicao_corda: Distribuição da corda ao longo da direção da envergadura como uma função de theta c(theta),
        onde theta é o ângulo polar em radianos.
        :param angulo_sustentacao_nula: Ângulo de ataque para sustentação nula.
        :return:
        """
        self.razao_aspecto = razao_aspecto
        self.razao_afilamento = razao_afilamento
        self.area = area
        self.distribuicao_corda = distribuicao_corda
        self.angulo_sustentacao_nula = angulo_sustentacao_nula

        # Calcular parâmetros geométricos auxiliares.
        self.envergadura = np.sqrt(self.razao_aspecto * self.area)  # Envergadura da asa.

    @staticmethod
    def obter_angulo_sustentacao_nula(entrada, theta):
        """
        Obter o ângulo de sustentação nula.
        :param entrada: Entrada do usuário. Pode ser uma função definindo o ângulo de sustentação nula como uma função do
        ângulo da estação ou uma constante.
        :param theta: Ângulo no qual o ângulo de sustentação nula deve ser avaliado.
        :return: Ângulo de sustentação nula. As unidades dependerão da entrada do usuário.
        """
        if hasattr(entrada, '__call__'):  # Verificar se a entrada é uma função.
            return entrada(theta)
        else:
            return entrada

    @staticmethod
    def obter_angulo_ataque(entrada, theta):
        """
        Obter o ângulo de ataque.
        :param entrada: Entrada do usuário para o ângulo de ataque. Pode ser uma função avaliável alpha(theta), onde
        theta é um ângulo da estação, ou pode ser uma constante em radianos.
        :param theta: Ângulo da estação em radianos.
        :return:
        """
        if hasattr(entrada, '__call__'):  # Verificar se a entrada é uma função.
            return entrada(theta)
        else:
            return entrada

    def definir_sistema(self):
        """
        Definir o sistema vindo da equação fundamental da linha de sustentação de Prandtl considerando os termos desejados
        pelo usuário.
        :return:
        """
        # Definir os símbolos dos termos de Fourier.
        termos_dict = dict()
        for i in self.termos_considerados:
            termos_dict[f'A{i}'] = sp.Symbol(f'A{i}')

        self.sistema = np.array([])

        # Definir a equação da linha de sustentação.
        for theta in self.angulos_estacoes:
            # Calcular o comprimento da corda na estação dada.
            c_theta = self.distribuicao_corda(theta)

            # Definir os termos de Fourier
            f1 = sp.Add(*[termos_dict[f'A{str(int(n))}'] * sp.sin(n * theta) for n in np.linspace(
                self.termos_considerados[0], self.termos_considerados[-1], len(self.termos_considerados))])

            f2 = sp.Add(*[n * termos_dict[f'A{str(int(n))}'] * (sp.sin(n * theta)) / (sp.sin(theta))
                          for n in np.linspace(self.termos_considerados[0], self.termos_considerados[-1],
                                               len(self.termos_considerados))])

            # Definir as equações Sympy.
            self.sistema = np.append(self.sistema, sp.Eq((2 * self.envergadura) / (sp.pi * c_theta) * f1 +
                                                         TeoriaLinhaSustentação.obter_angulo_sustentacao_nula(
                                                             self.angulo_sustentacao_nula, theta) +
                                                         f2,
                                                         TeoriaLinhaSustentação.obter_angulo_ataque(
                                                             self.angulo_ataque, theta)))
        self.simbolos = tuple(list(termos_dict.values()))
        self.sistema = tuple(self.sistema)

    def resolver(self, angulo_ataque, angulos_estacoes, termos_considerados):
        """
        Resolver para os coeficientes de Fourier considerados dado um ângulo de ataque e ângulos das estações, que vêm da
        mudança de variável y = -b/2 * cos(theta).
        :param angulo_ataque: Ângulo de ataque em radianos.
        :param angulos_estacoes: Lista contendo os ângulos das estações em radianos.
        :param termos_considerados: Lista contendo os termos considerados para a série de Fourier. Deve ter o mesmo
        comprimento que a variável angulos_estacoes.
        :return:
        """
        assert len(angulos_estacoes) == len(termos_considerados), 'As variáveis angulos_estacoes e termos_considerados não têm o mesmo comprimento.'

        self.angulo_ataque = angulo_ataque
        self.angulos_estacoes = angulos_estacoes
        self.termos_considerados = termos_considerados

        # Definir o sistema da linha de sustentação com os termos considerados.
        self.definir_sistema()

        # Resolver o sistema.
        resposta = sp.solve(self.sistema, self.simbolos)

        # Extrair os coeficientes.
        for chave, valor in resposta.items():
            self.coeficientes_fourier[str(chave)] = valor

    def calcular_coeficiente_sustentacao(self):
        """
        Calcular o coeficiente de sustentação da asa inteira.
        :return: Coeficiente de sustentação da asa inteira.
        """
        return self.coeficientes_fourier[str(sp.Symbol('A1'))] * np.pi * self.razao_aspecto

    def calcular_parametro_arrasto_induzido(self):
        """
        Calcular o parâmetro de arrasto induzido, conforme Anderson.
        :return: Parâmetro de arrasto induzido.
        """
        termos_lista = self.termos_considerados[1:]

        termo = sp.Add(*[n * (self.coeficientes_fourier[str(sp.Symbol(f'A{str(int(n))}'))] /
                             self.coeficientes_fourier[str(sp.Symbol('A1'))]) ** 2 for n in
                          np.linspace(termos_lista[0], termos_lista[-1], len(termos_lista))]).doit()

        return termo

    @staticmethod
    def calcular_coeficiente_oswald(parametro_arrasto_induzido):
        """
        Calcular o coeficiente de Oswald a partir do parâmetro de arrasto induzido.
        :param parametro_arrasto_induzido: O parâmetro de arrasto induzido.
        :return: Coeficiente de Oswald.
        """
        return (1 + parametro_arrasto_induzido) ** (-1)

    def calcular_coeficiente_arrasto_induzido(self, coeficiente_oswald=None, parametro_arrasto_induzido=None):
        """
        Calcular o coeficiente de arrasto induzido dado o coeficiente de sustentação e o coeficiente de Oswald/param. de arrasto.
        :param coeficiente_oswald: Coeficiente de Oswald. Opcional, padrão é None.
        :param parametro_arrasto_induzido: Parâmetro de arrasto induzido. Opcional, padrão é None.
        :return: O coeficiente de arrasto induzido.
        """
        C_L = self.coeficientes_fourier['A1'] * np.pi * self.razao_aspecto
        if coeficiente_oswald is not None:
            return C_L ** 2 / (np.pi * coeficiente_oswald * self.razao_aspecto)
        elif parametro_arrasto_induzido is not None:
            return C_L ** 2 / (np.pi * self.razao_aspecto) * (1 + parametro_arrasto_induzido)
        



# Classe ajustada para voo em formação
class TeoriaLinhaSustentacaoFormacao(TeoriaLinhaSustentação):
    def __init__(self, num_aeronaves, c_d0=0.02):
        """
        Implementação da Teoria da Linha de Sustentação de Prandtl para voo em formação.
        :param num_aeronaves: Número de aeronaves na formação.
        :param c_d0: Coeficiente de arrasto parasita (constante).
        """
        super().__init__()
        self.num_aeronaves = num_aeronaves
        self.c_d0 = c_d0
        self.coeficientes_sustentacao_formacao = [0.0] * num_aeronaves
        self.coeficientes_arrasto_induzido = [0.0] * num_aeronaves
        self.coeficientes_arrasto_total = [0.0] * num_aeronaves
        self.reducao_arrasto_percentual = []

    def resolver_formacao(self, angulo_ataque, angulos_estacoes, termos_considerados, distancias):
        """
        Resolver o problema de voo em formação considerando o efeito upwash.
        :param angulo_ataque: Ângulo de ataque da aeronave líder (radianos).
        :param angulos_estacoes: Lista de ângulos das estações (radianos).
        :param termos_considerados: Termos da série de Fourier.
        :param distancias: Distâncias longitudinais (metros) entre as aeronaves.
        """
        self.resolver(angulo_ataque, angulos_estacoes, termos_considerados)
        cl_lider = float(self.calcular_coeficiente_sustentacao())
        parametro_arrasto_induzido = float(self.calcular_parametro_arrasto_induzido())
        coeficiente_oswald = float(self.calcular_coeficiente_oswald(parametro_arrasto_induzido))
        cdi_lider = cl_lider**2 / (np.pi * coeficiente_oswald * self.razao_aspecto)
        cd_total_lider = cdi_lider + self.c_d0

        self.coeficientes_sustentacao_formacao[0] = cl_lider
        self.coeficientes_arrasto_induzido[0] = cdi_lider
        self.coeficientes_arrasto_total[0] = cd_total_lider

        # Resolver para as aeronaves seguidoras
        for i in range(1, self.num_aeronaves):
            delta_alpha = 0.15 * (self.coeficientes_sustentacao_formacao[i - 1] / (np.pi * self.razao_aspecto)) * (self.envergadura / distancias[i - 1])
            angulo_ataque_ajustado = angulo_ataque + delta_alpha

            # Resolver para a aeronave seguidora
            self.resolver(angulo_ataque_ajustado, angulos_estacoes, termos_considerados)
            cl_seguidora = float(self.calcular_coeficiente_sustentacao())
            cdi_seguidora = cl_seguidora**2 / (np.pi * coeficiente_oswald * self.razao_aspecto)

            # Ajuste baseado na rotação do vetor força
            delta_l = cdi_seguidora * np.sin(delta_alpha)
            delta_d = cl_seguidora * np.sin(delta_alpha)
            cl_seguidora += delta_l
            cdi_seguidora -= delta_d

            cd_total_seguidora = cdi_seguidora + self.c_d0

            # Armazenar os resultados
            self.coeficientes_sustentacao_formacao[i] = cl_seguidora
            self.coeficientes_arrasto_induzido[i] = cdi_seguidora
            self.coeficientes_arrasto_total[i] = cd_total_seguidora

        # Calcular a redução de arrasto em relação ao voo solo
        arrasto_base = cd_total_lider
        self.reducao_arrasto_percentual = [
            (arrasto_base - self.coeficientes_arrasto_total[i]) / arrasto_base * 100
            for i in range(self.num_aeronaves)
        ]

    def obter_resultados(self):
        """
        Retorna os resultados da formação de voo em um formato estruturado.
        """
        return {
            f"Aeronave {i + 1}": {
                "Coeficiente de Sustentação (C_L)": self.coeficientes_sustentacao_formacao[i],
                "Coeficiente de Arrasto Induzido (C_Di)": self.coeficientes_arrasto_induzido[i],
                "Coeficiente de Arrasto Total (C_D)": self.coeficientes_arrasto_total[i],
                "Redução de Arrasto (%)": self.reducao_arrasto_percentual[i],
            }
            for i in range(self.num_aeronaves)
        }




