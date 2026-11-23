from typing import Literal

from pydantic import BaseModel, Field


class PacienteRequest(BaseModel):
    """Atributos clínicos de entrada, com os mesmos nomes das colunas do dataset."""

    Age: int = Field(
        ..., ge=18, le=100,
        description="Idade do paciente em anos.",
        examples=[45],
    )
    Sex: Literal["M", "F"] = Field(
        ...,
        description="Sexo do paciente: M (masculino) ou F (feminino).",
        examples=["M"],
    )
    ChestPainType: Literal["TA", "ATA", "NAP", "ASY"] = Field(
        ...,
        description="Tipo de dor no peito: TA (angina típica), ATA (angina atípica), NAP (dor não anginosa) ou ASY (assintomático).",
        examples=["ATA"],
    )
    RestingBP: int = Field(
        ..., ge=0, le=250,
        description="Pressão arterial em repouso, em mm Hg.",
        examples=[120],
    )
    Cholesterol: int = Field(
        ..., ge=0, le=700,
        description="Nível de colesterol sérico, em mg/dl.",
        examples=[200],
    )
    FastingBS: int = Field(
        ..., ge=0, le=1,
        description="Glicemia em jejum acima de 120 mg/dl: 1 = sim, 0 = não.",
        examples=[0],
    )
    RestingECG: Literal["Normal", "ST", "LVH"] = Field(
        ...,
        description="Resultado do eletrocardiograma em repouso: Normal, ST (anomalia de onda ST-T) ou LVH (hipertrofia ventricular esquerda provável).",
        examples=["Normal"],
    )
    MaxHR: int = Field(
        ..., ge=60, le=202,
        description="Frequência cardíaca máxima atingida durante o exercício, em bpm.",
        examples=[150],
    )
    ExerciseAngina: Literal["Y", "N"] = Field(
        ...,
        description="Angina induzida por exercício: Y (sim) ou N (não).",
        examples=["N"],
    )
    Oldpeak: float = Field(
        ..., ge=-3.0, le=7.0,
        description="Depressão do segmento ST induzida por exercício, em relação ao repouso.",
        examples=[1.0],
    )
    ST_Slope: Literal["Up", "Flat", "Down"] = Field(
        ...,
        description="Inclinação do segmento ST no pico do exercício: Up, Flat ou Down.",
        examples=["Up"],
    )


class PacienteResponse(BaseModel):
    """Resultado da predição. Não constitui diagnóstico médico."""

    categoria_prevista: str = Field(
        ...,
        description="Classificação prevista pelo modelo. Uso acadêmico, não é diagnóstico médico.",
        examples=["Sem indicativo de doença cardíaca"],
    )
    score_confianca: float = Field(
        ..., ge=0.0, le=1.0,
        description="Maior probabilidade entre as classes, obtida via predict_proba.",
        examples=[0.9123],
    )