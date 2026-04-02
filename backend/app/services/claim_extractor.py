from groq import Groq
import ast

client = Groq(api_key="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")


def load_prompt():
    with open("app/prompts/claim_prompt.txt", "r") as f:
        return f.read()


def extract_claims(response_text: str):
    prompt_template = load_prompt()
    prompt = prompt_template.replace("{response}", response_text)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    output = completion.choices[0].message.content

    print("RAW OUTPUT:", output)  # 🔥 DEBUG

    try:
        claims = ast.literal_eval(output)
        return claims
    except Exception as e:
        print("PARSE ERROR:", e)
        
        # 🔥 fallback: manual extraction
        lines = output.split("\n")
        claims = [line.strip("- ").strip() for line in lines if line.strip()]
        
        return claims