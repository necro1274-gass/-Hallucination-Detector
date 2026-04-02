from app.services.claim_extractor import extract_claims
from app.services.search_service import search_claim
from app.services.verifier import verify_claim

def run_pipeline(response_text: str):
    results = []
    false_count = 0

    claims = extract_claims(response_text)

    for claim in claims:
        # 🚫 Skip bad claims
        if not claim or len(claim.strip()) < 10:
            continue

        search_results = search_claim(claim)
        evidence_text = " ".join([r["content"] for r in search_results])
        verification = verify_claim(claim, evidence_text)
        if verification["status"] == "false":
            false_count += 1

        results.append({
            "claim": claim,
            "verification": verification
        })

    total = len(claims)

    hallucination_score = (false_count / total) * 100 if total > 0 else 0

    return {
        "hallucination_score": hallucination_score,
        "total_claims": total,
        "false_claims": false_count,
        "results": results
    }