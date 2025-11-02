from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OntologyQuery:
    def __init__(self):
        self.sparql = SPARQLWrapper(settings.FUSEKI_ENDPOINT)
        self.sparql.setReturnFormat(JSON)
        self.namespace = "http://example.org/health#"
    
    def execute_query(self, query):
        """Execute SPARQL query and return results"""
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            return results
        except Exception as e:
            logger.error(f"SPARQL query error: {str(e)}")
            return {"results": {"bindings": []}}
    
    def get_all_patients(self):
        """Get all patients from ontology"""
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX health: <{self.namespace}>
        
        SELECT ?patient ?nom ?prenom ?email
        WHERE {{
            ?patient rdf:type health:Patient .
            OPTIONAL {{ ?patient health:nom ?nom }}
            OPTIONAL {{ ?patient health:prenom ?prenom }}
            OPTIONAL {{ ?patient health:email ?email }}
        }}
        """
        return self.execute_query(query)
    
    def get_traitements_for_maladie(self, maladie_nom):
        """Get all treatments for a specific disease"""
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX health: <{self.namespace}>
        
        SELECT ?traitement ?nomTraitement ?cout ?efficacite ?scoreCarbone
        WHERE {{
            ?maladie rdf:type health:Maladie ;
                     health:nomMaladie "{maladie_nom}" .
            ?traitement health:traite ?maladie ;
                       health:nomTraitement ?nomTraitement .
            OPTIONAL {{ ?traitement health:cout ?cout }}
            OPTIONAL {{ ?traitement health:efficacite ?efficacite }}
            OPTIONAL {{ 
                ?traitement health:aImpact ?impact .
                ?impact health:scoreCarbone ?scoreCarbone 
            }}
        }}
        ORDER BY ?scoreCarbone
        """
        return self.execute_query(query)
    
    def get_traitements_eco_responsables(self, score_max=5.0):
        """Get eco-friendly treatments below carbon score threshold"""
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX health: <{self.namespace}>
        
        SELECT ?nomTraitement ?scoreCarbone ?efficacite ?consommationEau ?recyclable
        WHERE {{
            ?traitement health:nomTraitement ?nomTraitement ;
                       health:efficacite ?efficacite ;
                       health:aImpact ?impact .
            ?impact health:scoreCarbone ?scoreCarbone .
            OPTIONAL {{ ?impact health:consommationEau ?consommationEau }}
            OPTIONAL {{ ?impact health:recyclable ?recyclable }}
            FILTER (?scoreCarbone <= {score_max})
        }}
        ORDER BY ?scoreCarbone
        """
        return self.execute_query(query)
    
    def get_medecins_by_specialite(self, specialite):
        """Get doctors by specialty"""
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX health: <{self.namespace}>
        
        SELECT ?medecin ?nom ?prenom ?anneesExperience
        WHERE {{
            ?medecin rdf:type health:{specialite} ;
                    health:nom ?nom ;
                    health:prenom ?prenom .
            OPTIONAL {{ ?medecin health:anneesExperience ?anneesExperience }}
        }}
        ORDER BY DESC(?anneesExperience)
        """
        return self.execute_query(query)
    
    def get_patient_full_profile(self, patient_email):
        """Get complete patient profile with diagnoses and treatments"""
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX health: <{self.namespace}>
        
        SELECT ?patient ?nom ?prenom ?maladie ?traitement ?medecin
        WHERE {{
            ?patient rdf:type health:Patient ;
                    health:email "{patient_email}" ;
                    health:nom ?nom ;
                    health:prenom ?prenom .
            OPTIONAL {{
                ?patient health:diagnostiquePour ?maladie .
                ?maladie health:nomMaladie ?nomMaladie .
            }}
            OPTIONAL {{
                ?patient health:recoit ?traitement .
                ?traitement health:nomTraitement ?nomTraitement .
            }}
        }}
        """
        return self.execute_query(query)
    
    def compare_traitements_impact(self, maladie_nom):
        """Compare treatments for same disease by eco-efficiency ratio"""
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX health: <{self.namespace}>
        
        SELECT ?nomTraitement ?scoreCarbone ?efficacite ?cout
               ((?efficacite / ?scoreCarbone) as ?ratioEfficaciteImpact)
        WHERE {{
            ?maladie health:nomMaladie "{maladie_nom}" .
            ?traitement health:traite ?maladie ;
                       health:nomTraitement ?nomTraitement ;
                       health:efficacite ?efficacite ;
                       health:cout ?cout ;
                       health:aImpact ?impact .
            ?impact health:scoreCarbone ?scoreCarbone .
            FILTER (?scoreCarbone > 0)
        }}
        ORDER BY DESC(?ratioEfficaciteImpact)
        """
        return self.execute_query(query)
    
    def get_treatment_alternatives_by_disease(self, maladie_nom):
        """
        SEMANTIC REASONING: Find all treatment pairs for same disease
        and calculate differences in environmental impact and efficacy.
        This demonstrates graph pattern matching that's complex in SQL.
        """
        query = f"""
        PREFIX health: <{self.namespace}>
        
        SELECT ?maladie ?traitement1 ?score1 ?efficacite1 ?traitement2 ?score2 ?efficacite2
               ((?score1 - ?score2) as ?scoreDiff)
               ((?efficacite1 - ?efficacite2) as ?efficaciteDiff)
        WHERE {{
            ?m health:nomMaladie "{maladie_nom}" .
            
            ?t1 health:nomTraitement ?traitement1 ;
                health:traite ?m ;
                health:efficacite ?efficacite1 ;
                health:aImpact ?i1 .
            ?i1 health:scoreCarbone ?score1 .
            
            ?t2 health:nomTraitement ?traitement2 ;
                health:traite ?m ;
                health:efficacite ?efficacite2 ;
                health:aImpact ?i2 .
            ?i2 health:scoreCarbone ?score2 .
            
            ?m health:nomMaladie ?maladie .
            
            FILTER (?t1 != ?t2)
            FILTER (?score1 > ?score2)
        }}
        ORDER BY DESC(?scoreDiff)
        """
        return self.execute_query(query)
    
    def get_best_treatment_recommendation(self, maladie_nom, max_score=10):
        """
        SEMANTIC REASONING: Calculate eco-efficiency ratio inline.
        Recommends treatments with best balance of clinical efficacy
        and environmental sustainability.
        """
        query = f"""
        PREFIX health: <{self.namespace}>
        
        SELECT ?traitement ?score ?efficacite ?cout
               ((?efficacite / ?score) as ?ecoEfficiencyRatio)
        WHERE {{
            ?m health:nomMaladie "{maladie_nom}" .
            ?t health:nomTraitement ?traitement ;
               health:traite ?m ;
               health:efficacite ?efficacite ;
               health:cout ?cout ;
               health:aImpact ?i .
            ?i health:scoreCarbone ?score .
            
            FILTER (?score <= {max_score})
            FILTER (?efficacite > 70)
        }}
        ORDER BY DESC(?ecoEfficiencyRatio)
        LIMIT 5
        """
        return self.execute_query(query)
    
    def get_eco_conscious_doctors(self, min_experience=5, max_impact=5):
        """
        SEMANTIC REASONING: Multi-hop query across doctor -> treatment -> impact.
        Aggregates to find doctors who prescribe eco-friendly treatments.
        """
        query = f"""
        PREFIX health: <{self.namespace}>
        
        SELECT ?medecin ?nom ?prenom ?specialite ?experience 
               (COUNT(DISTINCT ?traitement) as ?ecoTreatmentCount)
               (AVG(?score) as ?avgScore)
        WHERE {{
            ?m health:nom ?nom ;
               health:prenom ?prenom ;
               health:specialite ?specialite ;
               health:anneesExperience ?experience ;
               health:prescrit ?traitement .
            
            ?traitement health:aImpact ?impact .
            ?impact health:scoreCarbone ?score .
            
            FILTER (?experience >= {min_experience})
            FILTER (?score <= {max_impact})
            
            BIND(?m as ?medecin)
        }}
        GROUP BY ?medecin ?nom ?prenom ?specialite ?experience
        ORDER BY DESC(?ecoTreatmentCount) ?avgScore
        """
        return self.execute_query(query)