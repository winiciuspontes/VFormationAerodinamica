from formation_analyzer import FormationAnalyzer
from result_plotter import ResultPlotter

def main():
    """Função principal que executa a análise aerodinâmica da formação de voo"""
    analyzer = FormationAnalyzer()
    
    results = analyzer.run_coefficient_analysis()
    
    plotter = ResultPlotter()
    
    plotter.plot_angle_sweep_results(*results)
    
    plotter.display_analysis_summary()

if __name__ == "__main__":
    main() 