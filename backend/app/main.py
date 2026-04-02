from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/test-claims")
def test_claims():
    sample_text = "Tesla was founded in 2003 by Elon Musk. It is headquartered in California."

    claims = extract_claims(sample_text)

    return {"claims": claims}

from app.services.search_service import search_claim

@app.get("/test-search")
def test_search():
    claim = "Tesla was founded in 2003"
    results = search_claim(claim)

    return {"results": results}

from app.services.verifier import verify_claim

@app.get("/test-verify")
def test_verify():
    claim = "Tesla was founded in 2003"

    evidence = "Tesla was founded in 2003 by Martin Eberhard and Marc Tarpenning."

    result = verify_claim(claim, evidence)

    return result

from app.services.orchestrator import run_pipeline

@app.post("/analyze")
def analyze(data: dict):
    response_text = data.get("response")

    results = run_pipeline(response_text)

    return {"results": results}