import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Réponds juste: OK"}]
    )
    assert response.choices[0].message.content is not None
    print("OpenAI API : OK")

def test_chromadb():
    import chromadb
    client = chromadb.Client()
    collection = client.create_collection("test")
    collection.add(documents=["Appartement Plateau Mont-Royal"], ids=["1"])
    results = collection.query(query_texts=["logement Montréal"], n_results=1)
    assert len(results["documents"][0]) > 0
    print(" ChromaDB : OK")

if __name__ == "__main__":
    test_openai()
    test_chromadb()
    print("\n🎉 Tous les tests passés — Sprint 0 complété !")
