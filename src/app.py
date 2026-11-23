from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Request

from src.schemas import PacienteRequest, PacienteResponse

# Caminho resolvido a partir da raiz do projeto, independente do diretório de execução
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_MODELO = RAIZ_PROJETO / "models" / "pipeline_rede_neural.joblib"

# Ordem das colunas esperadas pelo pipeline (mesma ordem do dataset, sem a coluna alvo)
COLUNAS_ENTRADA = [
    "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", "FastingBS",
    "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope",
]

CATEGORIAS = {
    0: "Sem indicativo de doença cardíaca",
    1: "Com indicativo de doença cardíaca",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # O modelo é carregado uma única vez, na inicialização do servidor
    if not CAMINHO_MODELO.exists():
        raise RuntimeError(f"Modelo não encontrado em {CAMINHO_MODELO}. Execute o notebook de treinamento antes de iniciar a API.")
    app.state.modelo = joblib.load(CAMINHO_MODELO)
    yield


app = FastAPI(
    title="Heart Disease Prediction — MLP API",
    description="API acadêmica e demonstrativa. Não constitui diagnóstico médico.",
    lifespan=lifespan,
)


@app.get("/diagnostico/modelo")
def diagnostico_modelo():
    return {
        "status": "operacional_v2",
        "framework": "FastAPI-Production",
        "modelo": "MLPClassifier",
    }


@app.post("/predict", response_model=PacienteResponse)
def predict(paciente: PacienteRequest, request: Request):
    modelo = request.app.state.modelo

    entrada = pd.DataFrame([paciente.model_dump()])[COLUNAS_ENTRADA]

    classe = int(modelo.predict(entrada)[0])
    probabilidades = modelo.predict_proba(entrada)[0]

    return PacienteResponse(
        categoria_prevista=CATEGORIAS[classe],
        score_confianca=float(probabilidades.max()),
    )