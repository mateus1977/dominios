# Ferramenta de Consulta de Domínios - Registro.br

Essa ferramenta automatiza a consulta de informações WHOIS de domínios no site do Registro.br, armazena os dados em um banco SQLite, exibe os resultados em uma interface web construída com Streamlit e permite salvar as informações em um arquivo Excel.

## Funcionalidades

- Consulta automática de detalhes WHOIS de domínios no site Registro.br.
- Armazenamento dos resultados em um banco de dados SQLite.
- Exibição dos dados em uma interface web com Streamlit.
- Carregamento de uma lista de domínios a partir de um arquivo Excel.
- Atualização do banco de dados com novos resultados.
- Classificação dos resultados de acordo com a data de expiração.

## Tecnologias Utilizadas

- **Python**
- **Selenium**: Para realizar a automação das consultas no site Registro.br.
- **SQLite**: Para armazenamento local dos dados dos domínios.
- **Streamlit**: Para criação da interface web interativa.
- **Pandas**: Para manipulação e exibição de dados em tabelas.

## Pré-requisitos

- **Python 3.9+** instalado em sua máquina.
- Driver para o navegador Chrome (Chromedriver) compatível com a versão do seu navegador.
- Arquivo Excel contendo os domínios a serem consultados (exemplo de estrutura no arquivo `dominios.xlsx`).

## Estrutura do Banco de Dados

A tabela `dominios` contém as seguintes colunas:
- `domain`: Nome do domínio.
- `status`: Status do domínio (e.g., publicado, congelado).
- `last_updated`: Data e hora da última atualização.
- `created`: Data de criação do domínio.
- `changed`: Data da última alteração.
- `expiration`: Data de expiração.
- `email`: Email associado ao domínio.

## Como Utilizar

1. **Clone o Repositório**
   ```bash
   git clone https://github.com/mateus1977/dominios.git
   cd dominios

2. **Instale as Dependências Recomendamos o uso de um ambiente virtual:**
   - python -m venv venv
   - source venv/bin/activate  # No Windows: venv\Scripts\activate
   - pip install -r requirements.txt

3. **Prepare o Arquivo Excel**

   - Crie ou edite um arquivo Excel chamado dominios.xlsx com as colunas:
   - dominio: O nome do domínio.
   - email: Email associado ao domínio.

 4. **Execute o Aplicativo**
    - streamlit run app.py

 5. **Atualize os Dados**
    - Clique no botão "Obter Status" para buscar os detalhes WHOIS dos domínios no arquivo Excel.
    - Veja os resultados atualizados na tabela exibida na interface web.
 

    
