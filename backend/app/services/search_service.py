from tavily import TavilyClient

# 🔑 paste your Tavily API key here
client = TavilyClient(api_key="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")


def search_claim(claim: str):
    response = client.search(
        query=claim,
        search_depth="advanced",
        max_results=5
    )

    results = []

    for r in response.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content")[:500]  # limit to 500 chars
        })

    return results