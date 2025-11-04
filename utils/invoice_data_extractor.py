import json

import fitz
from openai import OpenAI


def pdf_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text("text") for page in doc)
    

SYS_PROMPT = """You are an invoicing expert. Extract fields from the provided INVOICE TEXT and return STRICT JSON.

Fields (keys):
- creditor_invoice_reference: string or null (creditor's reference if present)
- creditor_name: string or null
- creditor_iban: string like 'BE..' or null (Belgian IBAN if present)
- structured_reference: string or null (Belgian structured format +++###/####/#####+++ if present; else null)
- total_amount_eur: number or null (use dot decimal; prefer the grand total / amount due; currency is EUR)

Rules:
- Invoices may be in Dutch, French, or English. Recognize common labels: 
  NL: factuurnummer, factuur, te betalen, totaal, mededeling, gestructureerde mededeling
  FR: numéro de facture, facture, montant dû, total, communication structurée
  EN: invoice number, amount due, total, structured communication, payment reference
- Prefer lines that indicate the final amount (total/amount due/te betalen/montant dû), not VAT or line subtotals.
- For structured reference, return the exact +++###/####/#####+++ string if present, otherwise null.
- If multiple totals appear (with and without VAT), choose the final to-pay amount.
- Return ONLY minified JSON. No extra text.
"""

USER_TMPL = "INVOICE TEXT:\n\n{body}\n\nExtract now."


def extract_invoice_data(pdf_path):
    body = pdf_text(pdf_path)
    client = OpenAI(
        base_url="https://unventuresome-gemma-melodyless.ngrok-free.dev/v1",
        api_key="workshop-demo"
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": USER_TMPL.format(body=body)},
        ]
    )

    data = json.loads(resp.choices[0].message.content)

    return data
