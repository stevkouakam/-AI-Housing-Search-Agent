from app.agents.extractor import extract_criteria
from app.models.schemas import TypeLogement


def test_coloc_meublee_montreal():
    result = extract_criteria("Coloc meublée Montréal max 700$ proche métro")
    assert result.ville == "Montréal"
    assert result.type_logement == TypeLogement.colocation
    assert result.meuble == True
    assert result.budget_max == 700
    assert "métro" in result.proximite
    print("Test 1 passé : coloc meublée Montréal")


def test_studio_quebec_budget_min_max():
    result = extract_criteria("Studio pas meublé à Québec, budget entre 500 et 800 dollars")
    assert result.ville == "Québec"
    assert result.type_logement == TypeLogement.studio
    assert result.meuble == False
    assert result.budget_min == 500
    assert result.budget_max == 800
    print("Test 2 passé : studio Québec avec budget min/max")


def test_appartement_quartier_specifique():
    result = extract_criteria("Appartement 2 chambres dans le Plateau-Mont-Royal, max 1200$")
    assert result.ville == "Montréal"
    assert result.type_logement == TypeLogement.appartement
    assert result.budget_max == 1200
    assert len(result.quartiers_preferes) > 0
    print("Test 3 passé : appartement avec quartier spécifique")


def test_chambre_disponibilite():
    result = extract_criteria("Chambre à louer à Montréal disponible en juillet, max 600$")
    assert result.ville == "Montréal"
    assert result.type_logement == TypeLogement.chambre
    assert result.budget_max == 600
    assert result.disponibilite is not None
    print("Test 4 passé : chambre avec disponibilité")


def test_criteres_manquants():
    result = extract_criteria("Je cherche quelque chose à Laval")
    assert result.ville == "Laval"
    assert result.type_logement is None
    assert result.budget_max is None
    assert result.meuble is None
    assert result.proximite == []
    print("Test 5 passé : critères manquants → null correctement")


if __name__ == "__main__":
    test_coloc_meublee_montreal()
    test_studio_quebec_budget_min_max()
    test_appartement_quartier_specifique()
    test_chambre_disponibilite()
    test_criteres_manquants()
    print("\n5/5 tests passés — Agent Extracteur validé !")
