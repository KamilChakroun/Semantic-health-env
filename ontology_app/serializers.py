from rest_framework import serializers
from .models import (
    Etablissement, Patient, Medecin, Maladie, Symptome,
    ImpactEnvironnemental, Medicament, Traitement, Examen,
    Diagnostic, Prescription
)

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    etablissement_nom = serializers.CharField(source='etablissement.nom_etablissement', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'

class MedecinSerializer(serializers.ModelSerializer):
    etablissement_nom = serializers.CharField(source='etablissement.nom_etablissement', read_only=True)
    
    class Meta:
        model = Medecin
        fields = '__all__'

class SymptomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptome
        fields = '__all__'

class MaladieSerializer(serializers.ModelSerializer):
    symptomes = SymptomeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Maladie
        fields = '__all__'

class ImpactEnvironnementalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactEnvironnemental
        fields = '__all__'

class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = '__all__'

class TraitementSerializer(serializers.ModelSerializer):
    maladie_nom = serializers.CharField(source='maladie.nom_maladie', read_only=True)
    impact_environnemental = ImpactEnvironnementalSerializer(read_only=True)
    medicaments = MedicamentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Traitement
        fields = '__all__'

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'

class DiagnosticSerializer(serializers.ModelSerializer):
    patient_nom = serializers.SerializerMethodField()
    maladie_nom = serializers.CharField(source='maladie.nom_maladie', read_only=True)
    medecin_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = Diagnostic
        fields = '__all__'
    
    def get_patient_nom(self, obj):
        return f"{obj.patient.prenom} {obj.patient.nom}"
    
    def get_medecin_nom(self, obj):
        return f"Dr. {obj.medecin.prenom} {obj.medecin.nom}"

class PrescriptionSerializer(serializers.ModelSerializer):
    traitement_nom = serializers.CharField(source='traitement.nom_traitement', read_only=True)
    patient_nom = serializers.SerializerMethodField()
    impact_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = '__all__'
    
    def get_patient_nom(self, obj):
        return f"{obj.diagnostic.patient.prenom} {obj.diagnostic.patient.nom}"
    
    def get_impact_score(self, obj):
        if obj.traitement.impact_environnemental:
            return float(obj.traitement.impact_environnemental.score_carbone)
        return None