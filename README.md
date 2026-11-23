# Heart Disease Prediction — MLP API

Projeto acadêmico da atividade AT2 de **Redes Neurais MLP e Deploy de API em Produção**. Ele treina uma rede neural multicamadas (MLP) com Scikit-Learn para classificar a presença ou ausência de indicativos de doença cardíaca a partir de dados clínicos, e disponibiliza o modelo por meio de uma API REST com FastAPI.

> **Aviso:** este projeto tem finalidade exclusivamente acadêmica e demonstrativa. **Não é uma ferramenta de diagnóstico médico** e não deve ser usado para decisões clínicas.

## Dataset

Heart Failure Prediction Dataset, disponível no Kaggle:

https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

O dataset possui 918 registros, 11 variáveis preditoras e a variável alvo `HeartDisease` (0 = sem indicativo, 1 = com indicativo). O dicionário completo das colunas está na primeira seção do notebook.

## Estrutura do projeto

```text
heart-disease-mlp-api/
├── data/
│   └── heart.csv                    # Base de dados obtida no Kaggle
├── models/
│   └── pipeline_rede_neural.joblib  # Pipeline completo (pré-processamento + MLP)
├── notebooks/
│   └── analise_treinamento.ipynb    # EDA, treinamento, métricas e exportação
├── src/
│   ├── __init__.py
│   ├── schemas.py                   # Contratos de entrada e saída (Pydantic)
│   └── app.py                       # API FastAPI, lifespan e rotas
├── pyproject.toml                   # Dependências gerenciadas com UV
├── uv.lock                          # Versões travadas das dependências
├── requisicoes.http                 # Testes de integração HTTP
└── README.md
```

## Pré-requisitos

- Python 3.12 ou superior
- [UV](https://docs.astral.sh/uv/) para gerenciar o ambiente e as dependências
- VS Code com a extensão **REST Client** (opcional, para executar o `requisicoes.http`)

No Windows, o UV pode ser instalado pelo PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Como reproduzir

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/heart-disease-mlp-api.git
cd heart-disease-mlp-api
```

### 2. Obter o dataset

Baixe o arquivo `heart.csv` pelo link do Kaggle indicado acima e coloque-o na pasta `data/`.

### 3. Instalar as dependências

Na raiz do projeto, execute:

```bash
uv sync
```

Esse comando cria o ambiente virtual em `.venv` e instala as versões travadas no `uv.lock`.

### 4. Treinar o modelo (opcional)

O repositório já contém o arquivo `models/pipeline_rede_neural.joblib`. Para treinar novamente, abra `notebooks/analise_treinamento.ipynb`, selecione o kernel do ambiente `.venv` e execute todas as células. O notebook regrava o modelo no caminho indicado.

### 5. Iniciar a API

```bash
uv run fastapi dev src/app.py
```

Quando aparecer `Application startup complete`, a API está pronta em `http://127.0.0.1:8000`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/diagnostico/modelo` | Retorna o status do serviço e o tipo de modelo |
| POST | `/predict` | Recebe os dados clínicos de um paciente e retorna a categoria prevista e a confiança |

A documentação interativa (Swagger UI) fica disponível em:

http://127.0.0.1:8000/docs

### Exemplo de requisição para `/predict`

```json
{
  "Age": 45,
  "Sex": "M",
  "ChestPainType": "ATA",
  "RestingBP": 120,
  "Cholesterol": 200,
  "FastingBS": 0,
  "RestingECG": "Normal",
  "MaxHR": 150,
  "ExerciseAngina": "N",
  "Oldpeak": 1.0,
  "ST_Slope": "Up"
}
```

Resposta esperada (HTTP 200):

```json
{
  "categoria_prevista": "Sem indicativo de doença cardíaca",
  "score_confianca": 0.7777596751327954
}
```

Entradas fora dos tipos ou limites definidos em `src/schemas.py` retornam HTTP 422, com o campo e o motivo da rejeição.

## Testes HTTP

O arquivo `requisicoes.http` contém cinco cenários:

1
