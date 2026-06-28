import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.models.schemas import SearchCriteria

load_dotenv()

SYSTEM_PROMPT = """
Tu es un expert en immobilier québécois. Ton rôle est d'analyser une demande
de logement écrite en langage naturel et d'en extraire les critères structurés.

Réponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni après.

Le JSON doit respecter exactement ce format :
{
  "ville": "nom de la ville (ex: Montréal, Québec)",
  "type_logement": "studio | chambre | colocation | appartement",
  "meuble": true | false | null,
  "budget_max": nombre ou null,
  "budget_min": nombre ou null,
  "proximite": ["liste", "de", "lieux"],
  "quartiers_preferes": ["liste", "de", "quartiers"],
  "disponibilite": "date ou null",
  "criteres_speciaux": ["liste", "de", "criteres"]
}

Règles importantes :
- Si une information n'est pas mentionnée, mets null ou une liste vide []
- Le budget est toujours en dollars canadiens (CAD)
- type_logement doit être exactement un des 4 choix ci-dessus
- Ne jamais inventer une information qui n'est pas dans le message
"""


def extract_criteria(query: str) -> SearchCriteria:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        temperature=0,
    )

    raw_json = response.choices[0].message.content
    data = json.loads(raw_json)
    return SearchCriteria(**data)
