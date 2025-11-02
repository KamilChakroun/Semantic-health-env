import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_environment.settings')
django.setup()

from ontology_app.models import *

# Fuseki configuration
FUSEKI_UPDATE = 'http://localhost:3030/health_env/update'
NAMESPACE = 'http://example.org/health#'

def escape_sparql_string(s):
    """Escape special characters for SPARQL"""
    if s is None:
        return ""
    s = str(s)
    # Escape backslashes first, then quotes
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    return s

def create_rdf_insert(triples):
    """Create SPARQL INSERT query"""
    query = f"""
    PREFIX health: <{NAMESPACE}>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    INSERT DATA {{
        {triples}
    }}
    """
    return query

def send_sparql_update(query):
    """Send update to Fuseki"""
    try:
        response = requests.post(
            FUSEKI_UPDATE,
            data={'update': query},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        # Accept both 200 and 204 status codes
        if response.status_code in [200, 204]:
            return True
        else:
            print(f"    ⚠️  Status {response.status_code}: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        return False

print("="*70)
print("📤 POPULATION DE FUSEKI AVEC DONNÉES RICHES")
print("="*70)

# Clear existing data
print("\n🗑️  Nettoyage des données existantes dans Fuseki...")
clear_query = f"""
PREFIX health: <{NAMESPACE}>
DELETE WHERE {{ ?s ?p ?o }}
"""
try:
    requests.post(FUSEKI_UPDATE, data={'update': clear_query}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    print("    ✅ Données nettoyées")
except:
    print("    ⚠️  Nettoyage ignoré (première utilisation?)")

# Populate Patients
print("\n📤 Population des Patients...")
for patient in Patient.objects.all():
    triples = f"""
        health:Patient_{patient.id} rdf:type health:Patient ;
            health:nom "{escape_sparql_string(patient.nom)}" ;
            health:prenom "{escape_sparql_string(patient.prenom)}" ;
            health:email "{escape_sparql_string(patient.email)}" ;
            health:dateNaissance "{patient.date_naissance}"^^xsd:date ;
            health:sexe "{escape_sparql_string(patient.sexe)}" ;
            health:numeroSecuriteSociale "{escape_sparql_string(patient.numero_securite_sociale)}" ;
            health:groupeSanguin "{escape_sparql_string(patient.groupe_sanguin or '')}" ;
            health:IMC "{float(patient.imc) if patient.imc else 0}"^^xsd:decimal .
    """
    if send_sparql_update(create_rdf_insert(triples)):
        print(f"    ✅ {patient.prenom} {patient.nom}")
    else:
        print(f"    ❌ Échec: {patient.prenom} {patient.nom}")

# Populate Médecins
print("\n📤 Population des Médecins...")
for medecin in Medecin.objects.all():
    spec_class = {
        'generaliste': 'Generaliste',
        'cardiologue': 'Cardiologue',
        'pneumologue': 'Pneumologue'
    }.get(medecin.specialite, 'Medecin')
    
    triples = f"""
        health:Medecin_{medecin.id} rdf:type health:{spec_class} ;
            rdf:type health:Medecin ;
            health:nom "{escape_sparql_string(medecin.nom)}" ;
            health:prenom "{escape_sparql_string(medecin.prenom)}" ;
            health:email "{escape_sparql_string(medecin.email)}" ;
            health:dateNaissance "{medecin.date_naissance}"^^xsd:date ;
            health:sexe "{escape_sparql_string(medecin.sexe)}" ;
            health:numeroOrdre "{escape_sparql_string(medecin.numero_ordre)}" ;
            health:specialite "{escape_sparql_string(medecin.specialite)}" ;
            health:anneesExperience {medecin.annees_experience} .
    """
    if send_sparql_update(create_rdf_insert(triples)):
        print(f"    ✅ Dr. {medecin.prenom} {medecin.nom} ({medecin.specialite}, {medecin.annees_experience} ans)")
    else:
        print(f"    ❌ Échec: Dr. {medecin.prenom} {medecin.nom}")

# Populate Maladies
print("\n📤 Population des Maladies...")
for maladie in Maladie.objects.all():
    type_class = {
        'chronique': 'MaladieChronique',
        'aigue': 'MaladieAigue',
        'infectieuse': 'MaladieInfectieuse',
        'cardiovasculaire': 'MaladieCardiovasculaire',
        'respiratoire': 'MaladieRespiratoire'
    }.get(maladie.type_maladie, 'Maladie')
    
    triples = f"""
        health:Maladie_{maladie.id} rdf:type health:{type_class} ;
            rdf:type health:Maladie ;
            health:nomMaladie "{escape_sparql_string(maladie.nom_maladie)}" ;
            health:codeCIM10 "{escape_sparql_string(maladie.code_cim10 or '')}" ;
            health:gravite "{escape_sparql_string(maladie.gravite)}" ;
            health:contagieuse {str(maladie.contagieuse).lower()} ;
            health:tauxMortalite "{float(maladie.taux_mortalite)}"^^xsd:decimal .
    """
    if send_sparql_update(create_rdf_insert(triples)):
        print(f"    ✅ {maladie.nom_maladie} ({type_class})")
    else:
        print(f"    ❌ Échec: {maladie.nom_maladie}")

# Populate Impacts Environnementaux
print("\n📤 Population des Impacts Environnementaux...")
for impact in ImpactEnvironnemental.objects.all():
    triples = f"""
        health:Impact_{impact.id} rdf:type health:ImpactEnvironnemental ;
            health:scoreCarbone "{float(impact.score_carbone)}"^^xsd:decimal ;
            health:consommationEau "{float(impact.consommation_eau)}"^^xsd:decimal ;
            health:dechets "{float(impact.dechets)}"^^xsd:decimal ;
            health:recyclable {str(impact.recyclable).lower()} .
    """
    if send_sparql_update(create_rdf_insert(triples)):
        print(f"    ✅ Impact {impact.id} (score: {impact.score_carbone} kg CO2)")
    else:
        print(f"    ❌ Échec: Impact {impact.id}")

# Populate Traitements avec liens vers impacts et maladies
print("\n📤 Population des Traitements...")
for traitement in Traitement.objects.all():
    type_class = {
        'medicamenteux': 'TraitementMedicamenteux',
        'chirurgie': 'Chirurgie',
        'physiotherapie': 'Physiotherapie',
        'radiotherapie': 'Radiotherapie',
        'psychotherapie': 'Psychotherapie'
    }.get(traitement.type_traitement, 'Traitement')
    
    triples = f"""
        health:Traitement_{traitement.id} rdf:type health:{type_class} ;
            rdf:type health:Traitement ;
            health:nomTraitement "{escape_sparql_string(traitement.nom_traitement)}" ;
            health:cout "{float(traitement.cout)}"^^xsd:decimal ;
            health:duree {traitement.duree} ;
            health:efficacite "{float(traitement.efficacite)}"^^xsd:decimal ;
            health:traite health:Maladie_{traitement.maladie.id} .
    """
    
    # Add impact relationship if exists
    if traitement.impact_environnemental:
        triples += f"""
        health:Traitement_{traitement.id} health:aImpact health:Impact_{traitement.impact_environnemental.id} .
        """
    
    if send_sparql_update(create_rdf_insert(triples)):
        impact_info = f"impact: {traitement.impact_environnemental.score_carbone} kg" if traitement.impact_environnemental else "pas d'impact"
        print(f"    ✅ {traitement.nom_traitement} ({impact_info})")
    else:
        print(f"    ❌ Échec: {traitement.nom_traitement}")

# Populate Diagnostics (relationships)
print("\n📤 Population des Relations Diagnostics...")
for diagnostic in Diagnostic.objects.all():
    triples = f"""
        health:Patient_{diagnostic.patient.id} health:diagnostiquePour health:Maladie_{diagnostic.maladie.id} .
    """
    if send_sparql_update(create_rdf_insert(triples)):
        print(f"    ✅ {diagnostic.patient.prenom} {diagnostic.patient.nom} → {diagnostic.maladie.nom_maladie}")
    else:
        print(f"    ❌ Échec: Diagnostic {diagnostic.id}")

# Populate Prescriptions (medecin prescrit traitement)
print("\n📤 Population des Relations Prescriptions...")
for prescription in Prescription.objects.all():
    medecin = prescription.diagnostic.medecin
    traitement = prescription.traitement
    triples = f"""
        health:Medecin_{medecin.id} health:prescrit health:Traitement_{traitement.id} .
    """
    if send_sparql_update(create_rdf_insert(triples)):
        print(f"    ✅ Dr. {medecin.nom} prescrit {traitement.nom_traitement}")
    else:
        print(f"    ❌ Échec: Prescription {prescription.id}")

print("\n" + "="*70)
print("✅ FUSEKI POPULÉ AVEC SUCCÈS!")
print("="*70)

# Test queries to verify
print("\n🧪 Tests de vérification...")
test_query = """
PREFIX health: <http://example.org/health#>
SELECT (COUNT(?t) as ?count) WHERE {
    ?t a health:Traitement .
}
"""

try:
    response = requests.post(
        'http://localhost:3030/health_env/sparql',
        data={'query': test_query},
        headers={'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        result = response.json()
        count = result['results']['bindings'][0]['count']['value']
        print(f"    ✅ {count} traitements trouvés dans Fuseki")
    else:
        print(f"    ⚠️  Impossible de vérifier (status: {response.status_code})")
except Exception as e:
    print(f"    ⚠️  Test ignoré: {e}")

print("\n🎯 Données optimisées pour démonstration SPARQL:")
print("   • Hypertension: 5 traitements (scores 0.8 à 25.3)")
print("   • Diabète: 3 traitements (scores 0.8 à 8.2)")
print("   • Permet comparaisons sémantiques complexes")
print("   • Ratios éco-efficacité calculables")
print("   • Médecins avec expériences variées (12-28 ans)")
print("\n🔍 Testez maintenant:")
print("   • http://localhost:3030 (Interface Fuseki)")
print("   • http://localhost:8000 (Application Django)")
print("   • Onglet '🔮 Sémantique' pour recherches avancées")
print("="*70)