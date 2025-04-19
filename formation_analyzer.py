import numpy as np
from wing import Wing

class FormationAnalyzer:
    """Classe responsável por analisar o comportamento aerodinâmico de formações de voo"""
    
    def __init__(self):
        """Inicializa o analisador de formações"""
        pass
    
    def angle_sweep_analysis(self, n_aircraft=3, alpha_range=None):
        """
        Analisa como os coeficientes variam com o ângulo de ataque para formação em V
        
        Parâmetros:
        n_aircraft -- número de aeronaves na formação
        alpha_range -- lista de ângulos de ataque para analisar (graus)
        
        Retorna:
        alphas -- lista de ângulos de ataque
        cls_isolated -- lista de CL para aeronave isolada
        cdis_isolated -- lista de CDi para aeronave isolada
        cls_formation -- lista de listas de CL para cada aeronave na formação
        cdis_formation -- lista de listas de CDi para cada aeronave na formação
        """
        if alpha_range is None:
            alpha_range = np.linspace(1, 10, 10)
        
        alphas = []
        cls_isolated = []
        cdis_isolated = []
        cls_formation = [[] for _ in range(n_aircraft)]
        cdis_formation = [[] for _ in range(n_aircraft)]
        
        print(f"\n=== Análise de Variação do Ângulo de Ataque (Formação com {n_aircraft} aeronaves) ===")
        
        for alpha in alpha_range:
            print(f"\nCalculando para ângulo de ataque α = {alpha:.1f}°...")
            
            isolated_wing = Wing(span=10, chord=1, alpha=alpha, name="Isolada")
            isolated_wing.calculate_elliptic_circulation()
            cl_isolated = isolated_wing.calculate_lift_coefficient()
            cdi_isolated = isolated_wing.calculate_induced_drag_coefficient()
            
            alphas.append(alpha)
            cls_isolated.append(cl_isolated)
            cdis_isolated.append(cdi_isolated)
            
            wings = []
            span = 10
            chord = 1
            spacing_x = span * 0.9
            spacing_y = span * 0.8
            
            for i in range(n_aircraft):
                if i == 0:
                    pos = [0, 0, 0]
                    adjusted_alpha = alpha
                else:
                    side = 1 if i % 2 == 1 else -1
                    row = (i + 1) // 2
                    pos = [-row * spacing_x, side * row * spacing_y, 0]
                    adjusted_alpha = alpha * 0.9
                
                wing = Wing(span=span, chord=chord, alpha=adjusted_alpha, 
                           position=pos, name=f"Aeronave {i+1}")
                wing.calculate_elliptic_circulation()
                wings.append(wing)
            
            for _ in range(10):
                for wing in wings:
                    other_wings = [w for w in wings if w != wing]
                    wing.calculate_coefficients(other_wings)
            
            for i, wing in enumerate(wings):
                cl = wing.calculate_lift_coefficient()
                cdi = wing.calculate_induced_drag_coefficient()
                cls_formation[i].append(cl)
                cdis_formation[i].append(cdi)
        
        return alphas, cls_isolated, cdis_isolated, cls_formation, cdis_formation
    
    def run_coefficient_analysis(self):
        """Executa análise de coeficientes aerodinâmicos com variação do ângulo de ataque"""
        alphas = np.linspace(1, 10, 10)
        
        results = self.angle_sweep_analysis(n_aircraft=3, alpha_range=alphas)
        
        return results 