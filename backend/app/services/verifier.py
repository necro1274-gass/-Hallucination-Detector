from groq import Groq
import json

client = Groq(api_key="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")


def load_prompt():
    with open("app/prompts/verification_prompt.txt", "r") as f:
        return f.read()


def verify_claim(claim: str, evidence: str):
    prompt_template = load_prompt()

    prompt = prompt_template.replace("{claim}", claim).replace("{evidence}", evidence)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    output = completion.choices[0].message.content

    print("VERIFIER OUTPUT:", output)  # debug

    try:
        result = json.loads(output)
        return result
    except:
        return {
            "status": "uncertain",
            "confidence": 0.5,
            "reason": "Parsing failed"
        }