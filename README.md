# 🛩️ Simulação de Formação de Voo com a Teoria da Linha de Sustentação de Prandtl

Este projeto visa simular os efeitos aerodinâmicos de uma formação de voo utilizando a **Teoria da Linha de Sustentação**. A implementação computacional calcula os coeficientes de sustentação $C_L$ e de arrasto induzido $C_{D,i}$ de cada aeronave na formação, levando em conta as interações aerodinâmicas entre elas.
---

## 📚 Fundamentos Teóricos

A **Teoria da Linha de Sustentação de Prandtl** assume uma distribuição contínua de vorticidade ao longo da envergadura de uma asa, considerando efeitos tridimensionais em voo.

### 📌 Coeficiente de Sustentação $C_L$

Para uma asa finita, o coeficiente de sustentação é dado por:

$$
C_L = \frac{a_0}{1 + \dfrac{a_0}{\pi \cdot AR \cdot e}} \cdot \alpha
$$

Onde:
- $a_0 = 2\pi$: derivada da curva de sustentação para um aerofólio fino em regime sub-sônico.
- $AR = \frac{b^2}{S}$: razão de aspecto (aspect ratio), com $b$ a envergadura e $S$ a área da asa.
- $e$: fator de eficiência (tipicamente entre 0.7 e 1.0).
- $\alpha$: ângulo de ataque em radianos.

---

### 📌 Coeficiente de Arrasto Induzido $C_{D,i}$

O arrasto induzido é uma consequência da sustentação gerada e da inclinação das linhas de corrente:

$$
C_{D,i} = \frac{C_L^2}{\pi \cdot AR \cdot e}
$$

---

### 📌 Circulação $\Gamma$ e Velocidade Induzida

A circulação $\Gamma$ em uma seção é estimada por:

$$
\Gamma = \frac{1}{2} \cdot V \cdot C_L \cdot c
$$

A velocidade induzida na direção vertical (downwash), causada pelas pontas de asa de outras aeronaves:

$$
w_i = \sum_j \left[ \frac{\Gamma_j}{4\pi} \cdot \frac{y_i - y_j}{(y_i - y_j)^2} \cdot \left( \frac{x_i - x_j}{\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}} + 1 \right) \right]
$$

Esse termo é somado ao ângulo de ataque efetivo:

$$
\alpha_{\text{efetivo}} = \alpha + \frac{w_i}{V}
$$

---

## ⚙️ Simulações e Resultados

Simulamos uma formação em **V** com 3 aeronaves:

- Líder
- Ala Esquerda
- Ala Direita

Todas com:
- Envergadura $b = 10\,m$
- $AR = 8$
- Eficiência $e = 1.0$
- Ângulo de ataque da líder: $5^\circ$
- Ângulo das alas variando entre $2^\circ$ e $6^\circ$ para análise paramétrica.

---

## Requisitos

Certifique-se de ter instalado o Python (versão >= 3.8). As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```


```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git

# Navegue para o diretório do projeto
cd seu-repositorio

python main.py

```


# Licença

MIT License

Copyright (c) 2024 Winicius Pontes Ramos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Autor

**Winicius Pontes Ramos**  
Universidade Federal do ABC (UFABC)  

**Tema do Projeto:**  
*Estudo do Impacto de Formação em Voo nos Coeficientes de Sustentação e Arrasto Induzido Utilizando a Teoria de Sustentação de Prandtl*