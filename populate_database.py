# populate_database.py
# Rich dataset designed to showcase semantic search advantages

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_environment.settings')
django.setup()

from ontology_app.models import *

print("🗑️  Nettoyage de la base de données...")
Prescription.objects.all().delete()
Diagnostic.objects.all().delete()
Traitement.objects.all().delete()
Examen.objects.all().delete()
ImpactEnvironnemental.objects.all().delete()
Medicament.objects.all().delete()
Symptome.objects.all().delete()
Maladie.objects.all().delete()
Medecin.objects.all().delete()
Patient.objects.all().delete()
Etablissement.objects.all().delete()

print("🏥 Création des établissements...")
etablissements = [
    Etablissement.objects.create(
        nom_etablissement="Hôpital Central de Paris",
        adresse_etablissement="12 Rue de la Santé, 75014 Paris",
        type_etablissement="hopital",
        capacite=500,
        certifications="ISO 9001, HAS"
    ),
    Etablissement.objects.create(
        nom_etablissement="Clinique Verte Saint-Jean",
        adresse_etablissement="45 Avenue des Champs, 75008 Paris",
        type_etablissement="clinique",
        capacite=100,
        certifications="HAS, Éco-Label"
    ),
    Etablissement.objects.create(
        nom_etablissement="Cabinet Médical des Lilas",
        adresse_etablissement="8 Rue des Lilas, 75019 Paris",
        type_etablissement="cabinet",
        capacite=20
    ),
]

print("👨‍⚕️ Création des médecins...")
medecins = [
    # Généralistes
    Medecin.objects.create(
        nom="Dubois", prenom="Marie",
        date_naissance=date(1975, 3, 15), sexe="F",
        email="marie.dubois@hospital.fr", telephone="0145678901",
        adresse="15 Rue de la République, Paris",
        numero_ordre="75123456", specialite="generaliste",
        annees_experience=20, etablissement=etablissements[2]
    ),
    Medecin.objects.create(
        nom="Rousseau", prenom="François",
        date_naissance=date(1980, 6, 10), sexe="M",
        email="francois.rousseau@hospital.fr", telephone="0145678904",
        adresse="30 Rue Victor Hugo, Paris",
        numero_ordre="75456789", specialite="generaliste",
        annees_experience=15, etablissement=etablissements[2]
    ),
    
    # Cardiologues
    Medecin.objects.create(
        nom="Martin", prenom="Pierre",
        date_naissance=date(1968, 7, 22), sexe="M",
        email="pierre.martin@hospital.fr", telephone="0145678902",
        adresse="22 Boulevard Haussmann, Paris",
        numero_ordre="75234567", specialite="cardiologue",
        annees_experience=28, etablissement=etablissements[0]
    ),
    Medecin.objects.create(
        nom="Lefevre", prenom="Catherine",
        date_naissance=date(1972, 11, 5), sexe="F",
        email="catherine.lefevre@hospital.fr", telephone="0145678905",
        adresse="18 Avenue Foch, Paris",
        numero_ordre="75567890", specialite="cardiologue",
        annees_experience=23, etablissement=etablissements[0]
    ),
    
    # Pneumologues
    Medecin.objects.create(
        nom="Bernard", prenom="Sophie",
        date_naissance=date(1982, 11, 8), sexe="F",
        email="sophie.bernard@hospital.fr", telephone="0145678903",
        adresse="33 Rue de Rivoli, Paris",
        numero_ordre="75345678", specialite="pneumologue",
        annees_experience=12, etablissement=etablissements[1]
    ),
]

print("👤 Création des patients...")
patients = [
    Patient.objects.create(
        nom="Dupont", prenom="Jean",
        date_naissance=date(1978, 5, 12), sexe="M",
        email="jean.dupont@email.fr", telephone="0612345678",
        adresse="10 Rue de la Paix, Paris",
        numero_securite_sociale="178055012345678",
        imc=24.5, groupe_sanguin="A+", allergies="Pénicilline",
        etablissement=etablissements[0]
    ),
    Patient.objects.create(
        nom="Moreau", prenom="Claire",
        date_naissance=date(1985, 9, 23), sexe="F",
        email="claire.moreau@email.fr", telephone="0623456789",
        adresse="25 Avenue Montaigne, Paris",
        numero_securite_sociale="285099012345679",
        imc=22.1, groupe_sanguin="O+", allergies="",
        etablissement=etablissements[1]
    ),
    Patient.objects.create(
        nom="Petit", prenom="Robert",
        date_naissance=date(1960, 2, 17), sexe="M",
        email="robert.petit@email.fr", telephone="0634567890",
        adresse="50 Rue du Faubourg Saint-Honoré, Paris",
        numero_securite_sociale="160026012345680",
        imc=27.8, groupe_sanguin="B+", allergies="Lactose",
        etablissement=etablissements[0]
    ),
    Patient.objects.create(
        nom="Laurent", prenom="Marie",
        date_naissance=date(1990, 3, 8), sexe="F",
        email="marie.laurent@email.fr", telephone="0645678901",
        adresse="12 Boulevard Saint-Michel, Paris",
        numero_securite_sociale="290038012345681",
        imc=21.5, groupe_sanguin="A-", allergies="",
        etablissement=etablissements[1]
    ),
]

print("🦠 Création des maladies...")
maladies = [
    # Maladies Cardiovasculaires (pour démontrer comparaison traitements)
    Maladie.objects.create(
        nom_maladie="Hypertension Artérielle", code_cim10="I10",
        type_maladie="cardiovasculaire", gravite="moderee",
        taux_mortalite=5.2, contagieuse=False,
        description="Pression artérielle élevée de façon chronique"
    ),
    Maladie.objects.create(
        nom_maladie="Insuffisance Cardiaque", code_cim10="I50",
        type_maladie="cardiovasculaire", gravite="grave",
        taux_mortalite=18.5, contagieuse=False,
        description="Incapacité du cœur à pomper suffisamment de sang"
    ),
    
    # Maladies Chroniques
    Maladie.objects.create(
        nom_maladie="Diabète de Type 2", code_cim10="E11",
        type_maladie="chronique", gravite="moderee",
        taux_mortalite=3.8, contagieuse=False,
        description="Trouble métabolique caractérisé par une hyperglycémie"
    ),
    
    # Maladies Respiratoires
    Maladie.objects.create(
        nom_maladie="Asthme Chronique", code_cim10="J45",
        type_maladie="respiratoire", gravite="moderee",
        taux_mortalite=1.2, contagieuse=False,
        description="Maladie inflammatoire chronique des voies respiratoires"
    ),
    Maladie.objects.create(
        nom_maladie="Bronchite Chronique", code_cim10="J42",
        type_maladie="respiratoire", gravite="moderee",
        taux_mortalite=2.5, contagieuse=False,
        description="Inflammation persistante des bronches"
    ),
    
    # Maladies Infectieuses
    Maladie.objects.create(
        nom_maladie="Grippe Saisonnière", code_cim10="J11",
        type_maladie="infectieuse", gravite="legere",
        taux_mortalite=0.5, contagieuse=True,
        description="Infection virale aiguë des voies respiratoires"
    ),
]

print("🌍 Création des impacts environnementaux...")
# NOTE: Each impact will be created WITH its treatment (OneToOne relationship)
# We don't create them separately anymore

print("💊 Création des médicaments...")
medicaments = [
    Medicament.objects.create(nom_medicament="Lisinopril", type_medicament="anticoagulant", dosage="10mg", forme="Comprimé", fabricant="Laboratoires Pharma", effets_secondaires="Toux sèche, vertiges"),
    Medicament.objects.create(nom_medicament="Amlodipine", type_medicament="anticoagulant", dosage="5mg", forme="Comprimé", fabricant="Cardio Pharma", effets_secondaires="Œdème des chevilles"),
    Medicament.objects.create(nom_medicament="Metformine", type_medicament="anti_inflammatoire", dosage="500mg", forme="Comprimé", fabricant="BioPharm", effets_secondaires="Troubles digestifs"),
    Medicament.objects.create(nom_medicament="Salbutamol", type_medicament="antibiotique", dosage="100mcg", forme="Inhalateur", fabricant="RespiraPharma", effets_secondaires="Tremblements, tachycardie"),
    Medicament.objects.create(nom_medicament="Paracétamol", type_medicament="analgesique", dosage="500mg", forme="Comprimé", fabricant="GeneriPharm", effets_secondaires="Rares"),
]

print("💉 Création des traitements (multiples pour même maladie)...")

# HYPERTENSION: Plusieurs alternatives avec impacts variés (pour démonstration comparaison)
traitements_hypertension = [
    Traitement.objects.create(
        nom_traitement="Modification du Mode de Vie", type_traitement="physiotherapie",
        cout=0.00, duree=180, efficacite=72.0,
        maladie=maladies[0], 
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=0.8, consommation_eau=5.0, dechets=0.1, recyclable=True),
        description="Programme d'exercice et régime alimentaire"
    ),
    Traitement.objects.create(
        nom_traitement="Lisinopril Standard", type_traitement="medicamenteux",
        cout=45.50, duree=90, efficacite=85.0,
        maladie=maladies[0],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=2.5, consommation_eau=15.0, dechets=0.5, recyclable=True),
        description="Traitement médicamenteux première ligne"
    ),
    Traitement.objects.create(
        nom_traitement="Amlodipine Standard", type_traitement="medicamenteux",
        cout=52.00, duree=90, efficacite=82.0,
        maladie=maladies[0],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=4.5, consommation_eau=22.0, dechets=1.2, recyclable=True),
        description="Alternative calcique"
    ),
    Traitement.objects.create(
        nom_traitement="Bithérapie Intensive", type_traitement="medicamenteux",
        cout=95.00, duree=120, efficacite=91.0,
        maladie=maladies[0],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=6.8, consommation_eau=45.0, dechets=3.5, recyclable=True),
        description="Combinaison de deux médicaments"
    ),
    Traitement.objects.create(
        nom_traitement="Traitement Hospitalier Complet", type_traitement="medicamenteux",
        cout=450.00, duree=30, efficacite=94.0,
        maladie=maladies[0],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=25.3, consommation_eau=300.0, dechets=35.0, recyclable=False),
        description="Traitement intensif avec suivi hospitalier"
    ),
]

# Associer médicaments
traitements_hypertension[1].medicaments.add(medicaments[0])
traitements_hypertension[2].medicaments.add(medicaments[1])
traitements_hypertension[3].medicaments.add(medicaments[0], medicaments[1])

# INSUFFISANCE CARDIAQUE: Alternatives chirurgie vs médicament
traitements_cardiaque = [
    Traitement.objects.create(
        nom_traitement="Traitement Médicamenteux Optimisé", type_traitement="medicamenteux",
        cout=180.00, duree=365, efficacite=76.0,
        maladie=maladies[1],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=8.2, consommation_eau=55.0, dechets=4.8, recyclable=False),
        description="Traitement médical de l'insuffisance cardiaque"
    ),
    Traitement.objects.create(
        nom_traitement="Pontage Coronarien", type_traitement="chirurgie",
        cout=25000.00, duree=60, efficacite=92.0,
        maladie=maladies[1],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=18.7, consommation_eau=200.0, dechets=22.0, recyclable=False),
        description="Intervention chirurgicale majeure"
    ),
]

# DIABÈTE: Alternatives avec impacts variés
traitements_diabete = [
    Traitement.objects.create(
        nom_traitement="Régime et Exercice", type_traitement="physiotherapie",
        cout=0.00, duree=365, efficacite=68.0,
        maladie=maladies[2],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=0.8, consommation_eau=5.0, dechets=0.1, recyclable=True),
        description="Approche naturelle sans médicaments"
    ),
    Traitement.objects.create(
        nom_traitement="Metformine Seule", type_traitement="medicamenteux",
        cout=32.00, duree=180, efficacite=78.0,
        maladie=maladies[2],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=3.2, consommation_eau=18.0, dechets=0.7, recyclable=True),
        description="Traitement première ligne du diabète"
    ),
    Traitement.objects.create(
        nom_traitement="Insulinothérapie", type_traitement="medicamenteux",
        cout=250.00, duree=365, efficacite=88.0,
        maladie=maladies[2],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=10.5, consommation_eau=70.0, dechets=6.2, recyclable=False),
        description="Injections quotidiennes d'insuline"
    ),
]

traitements_diabete[1].medicaments.add(medicaments[2])

# ASTHME: Alternatives écologiques vs standard
traitements_asthme = [
    Traitement.objects.create(
        nom_traitement="Inhalateur Écologique", type_traitement="medicamenteux",
        cout=28.50, duree=365, efficacite=82.0,
        maladie=maladies[3],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=1.5, consommation_eau=8.0, dechets=0.3, recyclable=True),
        description="Inhalateur à faible GES"
    ),
    Traitement.objects.create(
        nom_traitement="Inhalateur Standard", type_traitement="medicamenteux",
        cout=35.00, duree=365, efficacite=84.0,
        maladie=maladies[3],
        impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=12.0, consommation_eau=85.0, dechets=8.5, recyclable=False),
        description="Inhalateur conventionnel"
    ),
]

traitements_asthme[0].medicaments.add(medicaments[3])
traitements_asthme[1].medicaments.add(medicaments[3])

# BRONCHITE
Traitement.objects.create(
    nom_traitement="Antibiotiques Ciblés", type_traitement="medicamenteux",
    cout=45.00, duree=14, efficacite=86.0,
    maladie=maladies[4],
    impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=4.5, consommation_eau=22.0, dechets=1.2, recyclable=True),
    description="Traitement antibiotique de courte durée"
)

# GRIPPE
Traitement.objects.create(
    nom_traitement="Repos et Paracétamol", type_traitement="medicamenteux",
    cout=5.00, duree=7, efficacite=75.0,
    maladie=maladies[5],
    impact_environnemental=ImpactEnvironnemental.objects.create(score_carbone=0.8, consommation_eau=5.0, dechets=0.1, recyclable=True),
    description="Traitement symptomatique simple"
)

print("📋 Création des diagnostics...")
diagnostics = [
    Diagnostic.objects.create(patient=patients[0], maladie=maladies[0], medecin=medecins[2], notes="HTA modérée, recommandation éco-responsable"),
    Diagnostic.objects.create(patient=patients[1], maladie=maladies[3], medecin=medecins[4], notes="Asthme allergique bien contrôlé"),
    Diagnostic.objects.create(patient=patients[2], maladie=maladies[2], medecin=medecins[0], notes="Diabète de type 2 récent"),
    Diagnostic.objects.create(patient=patients[3], maladie=maladies[0], medecin=medecins[3], notes="HTA légère, patient jeune"),
    Diagnostic.objects.create(patient=patients[2], maladie=maladies[1], medecin=medecins[2], notes="Insuffisance cardiaque modérée"),
]

print("📝 Création des prescriptions...")
# Prescrire traitements éco-responsables
Prescription.objects.create(diagnostic=diagnostics[0], traitement=traitements_hypertension[1], posologie="1 comprimé matin à jeun", duree_prescription=90, renouvellement=True)
Prescription.objects.create(diagnostic=diagnostics[1], traitement=traitements_asthme[0], posologie="2 bouffées matin et soir", duree_prescription=365, renouvellement=True)
Prescription.objects.create(diagnostic=diagnostics[2], traitement=traitements_diabete[1], posologie="500mg 2x/jour avec repas", duree_prescription=180, renouvellement=True)
Prescription.objects.create(diagnostic=diagnostics[3], traitement=traitements_hypertension[0], posologie="Programme exercice 30min/jour", duree_prescription=180, renouvellement=False)

print("\n" + "="*70)
print("✅ BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS!")
print("="*70)
print(f"\n📊 Statistiques:")
print(f"   - {Etablissement.objects.count()} établissements")
print(f"   - {Patient.objects.count()} patients")
print(f"   - {Medecin.objects.count()} médecins")
print(f"   - {Maladie.objects.count()} maladies")
print(f"   - {Traitement.objects.count()} traitements")
print(f"   - {ImpactEnvironnemental.objects.count()} impacts environnementaux")
print(f"   - {Diagnostic.objects.count()} diagnostics")
print(f"   - {Prescription.objects.count()} prescriptions")

print("\n🌱 Traitements éco-responsables (score < 5):")
eco = Traitement.objects.filter(impact_environnemental__score_carbone__lt=5).order_by('impact_environnemental__score_carbone')
for t in eco:
    print(f"   ✓ {t.nom_traitement} - {t.impact_environnemental.score_carbone} kg CO2 - Efficacité: {t.efficacite}%")

print("\n🔍 Avantages pour recherche sémantique:")
print("   1. Hypertension a 5 traitements avec impacts variés (0.8 à 25.3 kg)")
print("   2. Permet de comparer alternatives éco vs standard")
print("   3. Multiples médecins avec expériences différentes")
print("   4. Ratios éco-efficacité calculables")
print("\n🎉 Données prêtes pour démonstration SPARQL!")
print("="*70)