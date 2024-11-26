# Estudo do Impacto de Formação em Voo nos Coeficientes de Sustentação e Arrasto Induzido Utilizando a Teoria de Sustentação de Prandtl

Este repositório contém a implementação de métodos baseados na Teoria da Linha de Sustentação de Prandtl, aplicada ao estudo de formações de voo. O objetivo principal é analisar como o voo em formação influencia os coeficientes de sustentação e arrasto induzido, destacando os ganhos em eficiência aerodinâmica.

---

## Embasamento Teórico

### Fundamentos da Teoria da Linha de Sustentação de Prandtl

A teoria de Prandtl modela a sustentação e o arrasto de asas finitas utilizando o conceito de **vórtices de ferradura**. A circulação ao longo da asa é representada por uma série de Fourier, permitindo determinar os coeficientes aerodinâmicos:

$$
\alpha(y_0) = \frac{\Gamma(y_0)}{\pi V_\infty c(y_0)} + \alpha_{L=0}(y_0) + \frac{1}{4\pi V_\infty} \int_{-b/2}^{b/2} \frac{d\Gamma/dy \, dy}{y_0 - y}
$$

A solução desta equação fornece:

1. **Coeficiente de Sustentação**:
   $$
   C_L = A_1 \pi \frac{b}{S} = A_1 \pi AR
   $$

2. **Coeficiente de Arrasto Induzido**:
   $$
   C_{D,i} = \frac{C_L^2}{\pi AR}
   $$

3. **Efeito do Alongamento**:
   $$
   C_D = C_{D,i} + C_{D,0}
   $$

### Voo em Formação e Benefícios Aerodinâmicos

No voo em formação, o efeito de **upwash** gerado pela asa líder proporciona ganhos de sustentação para as aeronaves seguidoras. Isso ocorre devido à rotação do vetor de força aerodinâmica, reduzindo o arrasto induzido:

$$
\Delta L = D \sin(\alpha), \quad \Delta D = L \sin(\alpha)
$$ 

A eficiência é mensurada pela redução percentual de arrasto:

$$
\text{Redução Percentual de Arrasto} = \frac{\Delta D}{D_{\text{base}}} \times 100
$$

### Aplicação Prática

Este trabalho tem o objetivo de demonstrar que a formação em V é ideal para maximizar a redução de arrasto, ajustando o espaçamento longitudinal e a inclinação relativa entre as aeronaves.

---

## Estrutura do Projeto

### Diretórios

- **`output/`**: Diretório para salvar gráficos e resultados gerados.
- **`requirements.txt`**: Arquivo com as dependências necessárias.

---

## Requisitos

Certifique-se de ter instalado o Python (versão >= 3.8). As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt


## Como Clonar o Repositório

Para obter uma cópia local do projeto, siga os passos abaixo:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git

# Navegue para o diretório do projeto
cd seu-repositorio




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