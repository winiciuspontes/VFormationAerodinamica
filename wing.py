import numpy as np

class Wing:
    """Classe que representa uma asa"""
    
    def __init__(self, span, chord, alpha, position=[0, 0, 0], name="Asa"):
        """
        Inicializa uma asa com parâmetros básicos
        
        Parâmetros:
        span -- envergadura da asa (m)
        chord -- corda da asa (m) - assumindo asa retangular por simplicidade
        alpha -- ângulo de ataque (graus)
        position -- posição [x, y, z] do centro da asa no espaço (m)
        name -- nome da asa para identificação
        """
        self.span = span
        self.chord = chord
        self.alpha = np.radians(alpha)
        self.position = np.array(position)
        self.name = name
        self.area = span * chord
        self.AR = span**2 / self.area
        
        
        self.n_points = 101
        self.y = np.linspace(-span/2, span/2, self.n_points)
        self.theta = np.arccos(-2 * self.y / span)
        
        
        self.A = np.zeros(20)
        
        self.e = 1.0
        
        self.a0 = 2.0 * np.pi
        
    def calculate_elliptic_circulation(self):
        """
        Calcula a distribuição elíptica de circulação ao longo da envergadura
        Γ(y) = Γ₀ √(1 - (2y/b)²)
        """
        y_norm = 2 * self.y / self.span
        
        gamma = np.sqrt(1 - y_norm**2)
        
        self.A = np.zeros(len(self.A))
        self.A[0] = self.alpha / (1 + np.pi * self.AR / (2 * self.a0))
        
        return gamma
        
    def calculate_coefficients(self, wings=None):
        """
        Calcula os coeficientes da série de Fourier para a distribuição de circulação
        incluindo efeitos de interferência de outras asas
        
        Parâmetros:
        wings -- lista de outras asas que interferem com esta (opcional)
        """
        n_terms = len(self.A)
        n_points = len(self.theta)
        
        M = np.zeros((n_points, n_terms))
        
        b = np.zeros(n_points)
        
        for i in range(n_points):
            theta_i = self.theta[i]
            
            for n in range(n_terms):
                M[i, n] = np.sin((n+1) * theta_i) * (1 + (n+1) * np.pi * self.AR / (2 * self.a0))
            
            b[i] = self.alpha * np.sin(theta_i)
            
            if wings is not None and len(wings) > 0:
                total_interference = 0
                for wing in wings:
                    if wing != self:
                        y_i = self.y[i]
                        interference = self.calculate_interference(wing, y_i)
                        total_interference += interference
                
                b[i] += total_interference * np.sin(theta_i)
        
        self.A = np.linalg.lstsq(M, b, rcond=None)[0]
        
        return self.A
    
    def calculate_interference(self, other_wing, y_point):
        """
        Calcula a interferência (ângulo induzido) causada por outra asa em um ponto específico
        usando um modelo baseado na teoria do vórtice de ferradura
        
        Valores positivos representam upwash, negativos downwash
        
        Parâmetros:
        other_wing -- a outra asa que causa interferência
        y_point -- posição ao longo da envergadura onde calcular a interferência
        
        Retorna:
        interference_angle -- o ângulo induzido (radianos)
        """
        rel_pos = self.position - other_wing.position
        
        rel_x = rel_pos[0]
        
        if abs(rel_x) < 0.1:  
            return 0
            
        rel_y = y_point - other_wing.position[1]
        rel_z = rel_pos[2]
        
        y_norm = 2 * rel_y / other_wing.span
        
        CL_other = other_wing.calculate_lift_coefficient()
        
        circulation = 0.5 * CL_other * other_wing.chord
        
        lateral_dist = abs(y_norm)
        
        total_dist = np.sqrt(rel_x**2 + rel_y**2 + rel_z**2)
        if total_dist < 0.1:
            return 0
        
        if rel_x > 0:
            left_tip_y = -other_wing.span/2
            dist_to_left = np.sqrt(rel_x**2 + (y_point - other_wing.position[1] - left_tip_y)**2 + rel_z**2)
            left_factor = 1 - rel_x/dist_to_left
            
            right_tip_y = other_wing.span/2
            dist_to_right = np.sqrt(rel_x**2 + (y_point - other_wing.position[1] - right_tip_y)**2 + rel_z**2)
            right_factor = 1 - rel_x/dist_to_right
            
            if lateral_dist < 1.0:
                sign = -1.0
                intensity_factor = np.cos(np.pi * y_norm / 2)
            else:
                sign = 1.0
                intensity_factor = 1.0 / (lateral_dist * np.pi)
                
            lateral_decay = 1.0 / (1.0 + (lateral_dist * np.pi)**2)
            
            x_norm = abs(rel_x) / other_wing.span
            
            longitudinal_decay = np.exp(-0.1 * x_norm)
        else:
            if lateral_dist < 1.0:
                sign = -1.0
                intensity_factor = np.cos(np.pi * y_norm / 2) * 0.1
            else:
                sign = 1.0
                intensity_factor = (1.0 / (lateral_dist * np.pi)) * 0.1
                
            lateral_decay = 1.0 / (1.0 + (lateral_dist * np.pi)**2)
            x_norm = abs(rel_x) / other_wing.span
            longitudinal_decay = np.exp(-0.2 * x_norm)
        
        interference_angle = sign * circulation * intensity_factor * lateral_decay * longitudinal_decay / (4 * np.pi)
        
        return interference_angle
    
    def calculate_lift_coefficient_basic(self):
        """Calcula o coeficiente de sustentação básico (sem considerar interferência)"""
        return np.pi * self.AR * self.A[0]
    
    def calculate_lift_coefficient(self):
        """Calcula o coeficiente de sustentação considerando todos os termos"""
        CL = self.calculate_lift_coefficient_basic()
        return CL
    
    def calculate_induced_drag_coefficient(self):
        """Calcula o coeficiente de arrasto induzido"""
        sum_term = 0
        for n in range(1, len(self.A)):
            sum_term += (n + 1) * (self.A[n] / self.A[0])**2
        
        CL = self.calculate_lift_coefficient()
        CDi = CL**2 / (np.pi * self.AR * self.e) * (1 + sum_term)
        
        return CDi 