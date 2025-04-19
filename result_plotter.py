import matplotlib.pyplot as plt
import numpy as np

class ResultPlotter:
    """Classe responsável por gerar visualizações dos resultados da análise aerodinâmica"""
    
    def __init__(self):
        """Inicializa o gerador de gráficos"""
        pass
    
    def plot_angle_sweep_results(self, alphas, cls_isolated, cdis_isolated, cls_formation, cdis_formation):
        """
        Plota os resultados da análise de variação de ângulo de ataque
        
        Parâmetros:
        alphas -- lista de ângulos de ataque
        cls_isolated -- lista de CL para aeronave isolada
        cdis_isolated -- lista de CDi para aeronave isolada
        cls_formation -- lista de listas de CL para cada aeronave na formação
        cdis_formation -- lista de listas de CDi para cada aeronave na formação
        """
        n_aircraft = len(cls_formation)
        
        eff_isolated = [cl/cdi for cl, cdi in zip(cls_isolated, cdis_isolated)]
        eff_formation = [[] for _ in range(n_aircraft)]
        
        for i in range(n_aircraft):
            eff_formation[i] = [cl/cdi for cl, cdi in zip(cls_formation[i], cdis_formation[i])]
        
        plt.figure(figsize=(10, 6))
        plt.plot(alphas, cls_isolated, 'ko-', linewidth=2, label='Aeronave Isolada')
        
        colors = ['b', 'g', 'r', 'c', 'm']
        for i in range(n_aircraft):
            plt.plot(alphas, cls_formation[i], f'{colors[i % len(colors)]}o-', linewidth=1.5, label=f'Aeronave {i+1}')
        
        plt.xlabel('Ângulo de Ataque (graus)', fontsize=12)
        plt.ylabel('Coeficiente de Sustentação (CL)', fontsize=12)
        plt.title('Coeficiente de Sustentação vs. Ângulo de Ataque', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("cl_vs_alpha.png", dpi=300)
        
        plt.figure(figsize=(10, 6))
        plt.plot(alphas, cdis_isolated, 'ko-', linewidth=2, label='Aeronave Isolada')
        
        for i in range(n_aircraft):
            plt.plot(alphas, cdis_formation[i], f'{colors[i % len(colors)]}o-', linewidth=1.5, label=f'Aeronave {i+1}')
        
        plt.xlabel('Ângulo de Ataque (graus)', fontsize=12)
        plt.ylabel('Coeficiente de Arrasto Induzido (CDi)', fontsize=12)
        plt.title('Coeficiente de Arrasto Induzido vs. Ângulo de Ataque', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("cdi_vs_alpha.png", dpi=300)
        
        plt.figure(figsize=(10, 6))
        plt.plot(alphas, eff_isolated, 'ko-', linewidth=2, label='Aeronave Isolada')
        
        for i in range(n_aircraft):
            plt.plot(alphas, eff_formation[i], f'{colors[i % len(colors)]}o-', linewidth=1.5, label=f'Aeronave {i+1}')
        
        plt.xlabel('Ângulo de Ataque (graus)', fontsize=12)
        plt.ylabel('Eficiência Aerodinâmica (CL/CDi)', fontsize=12)
        plt.title('Eficiência Aerodinâmica vs. Ângulo de Ataque', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("efficiency_vs_alpha.png", dpi=300)
        
        plt.figure(figsize=(10, 6))
        
        for i in range(n_aircraft):
            pct_improvement = [(eff_formation[i][j]/eff_isolated[j] - 1)*100 for j in range(len(alphas))]
            plt.plot(alphas, pct_improvement, f'{colors[i % len(colors)]}o-', linewidth=1.5, label=f'Aeronave {i+1}')
        
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        plt.xlabel('Ângulo de Ataque (graus)', fontsize=12)
        plt.ylabel('Melhoria na Eficiência (%)', fontsize=12)
        plt.title('Variação Percentual da Eficiência em Relação ao Voo Isolado', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("efficiency_improvement.png", dpi=300)
        
        print("\n=== Resultados Numéricos para Ângulo de Ataque = 5° ===")
        alpha_5_index = alphas.index(5.0) if 5.0 in alphas else np.argmin(np.abs(np.array(alphas) - 5.0))
        
        print(f"Aeronave Isolada: CL = {cls_isolated[alpha_5_index]:.4f}, CDi = {cdis_isolated[alpha_5_index]:.4f}, Eficiência = {eff_isolated[alpha_5_index]:.4f}")
        
        for i in range(n_aircraft):
            print(f"Aeronave {i+1}: CL = {cls_formation[i][alpha_5_index]:.4f}, CDi = {cdis_formation[i][alpha_5_index]:.4f}, Eficiência = {eff_formation[i][alpha_5_index]:.4f}")
            
            eff_improvement = (eff_formation[i][alpha_5_index]/eff_isolated[alpha_5_index] - 1)*100
            print(f"  Melhoria na Eficiência: {eff_improvement:.2f}%")
    
    def display_analysis_summary(self):
        """Exibe um resumo dos gráficos gerados"""
        print("\nAnálise concluída! Os seguintes gráficos foram gerados:")
        print("- cl_vs_alpha.png - Variação de CL com o ângulo de ataque")
        print("- cdi_vs_alpha.png - Variação de CDi com o ângulo de ataque")
        print("- efficiency_vs_alpha.png - Variação da eficiência com o ângulo de ataque")
        print("- efficiency_improvement.png - Melhoria na eficiência em relação ao voo isolado") 