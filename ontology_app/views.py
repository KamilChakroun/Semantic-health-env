
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Count, Avg
from .models import (
    Etablissement, Patient, Medecin, Maladie, Symptome,
    ImpactEnvironnemental, Medicament, Traitement, Examen,
    Diagnostic, Prescription
)
from .serializers import (
    EtablissementSerializer, PatientSerializer, MedecinSerializer,
    MaladieSerializer, SymptomeSerializer, ImpactEnvironnementalSerializer,
    MedicamentSerializer, TraitementSerializer, ExamenSerializer,
    DiagnosticSerializer, PrescriptionSerializer
)
from .sparql_queries import OntologyQuery

def index(request):
    """Render main application page"""
    return render(request, 'index.html')

class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        etablissement = self.get_object()
        return Response({
            'nombre_patients': etablissement.patients.count(),
            'nombre_medecins': etablissement.medecins.count(),
            'capacite': etablissement.capacite,
        })

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    @action(detail=True, methods=['get'])
    def diagnostics(self, request, pk=None):
        patient = self.get_object()
        diagnostics = patient.diagnostics.all()
        serializer = DiagnosticSerializer(diagnostics, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def profile_ontology(self, request, pk=None):
        patient = self.get_object()
        ontology = OntologyQuery()
        profile = ontology.get_patient_full_profile(patient.email)
        return Response(profile)

class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer
    
    @action(detail=False, methods=['get'])
    def by_specialite(self, request):
        specialite = request.query_params.get('specialite')
        if specialite:
            medecins = Medecin.objects.filter(specialite=specialite)
            serializer = self.get_serializer(medecins, many=True)
            return Response(serializer.data)
        return Response({"error": "specialite parameter required"}, status=400)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        medecin = self.get_object()
        return Response({
            'nombre_diagnostics': medecin.diagnostics.count(),
            'specialite': medecin.get_specialite_display(),
            'annees_experience': medecin.annees_experience,
        })

class MaladieViewSet(viewsets.ModelViewSet):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer
    
    @action(detail=True, methods=['get'])
    def traitements(self, request, pk=None):
        maladie = self.get_object()
        traitements = maladie.traitements.all()
        serializer = TraitementSerializer(traitements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def traitements_eco(self, request, pk=None):
        maladie = self.get_object()
        ontology = OntologyQuery()
        traitements = ontology.get_traitements_for_maladie(maladie.nom_maladie)
        return Response(traitements)
    
    @action(detail=True, methods=['get'])
    def compare_traitements(self, request, pk=None):
        maladie = self.get_object()
        ontology = OntologyQuery()
        comparison = ontology.compare_traitements_impact(maladie.nom_maladie)
        return Response(comparison)

class SymptomeViewSet(viewsets.ModelViewSet):
    queryset = Symptome.objects.all()
    serializer_class = SymptomeSerializer

class TraitementViewSet(viewsets.ModelViewSet):
    queryset = Traitement.objects.all()
    serializer_class = TraitementSerializer
    
    @action(detail=False, methods=['get'])
    def eco_responsables(self, request):
        """PostgreSQL query for eco-friendly treatments"""
        score_max = float(request.query_params.get('score_max', 5.0))
        traitements = Traitement.objects.filter(
            impact_environnemental__score_carbone__lte=score_max
        ).select_related('impact_environnemental', 'maladie')
        serializer = self.get_serializer(traitements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def eco_ontology(self, request):
        """SPARQL query for eco-friendly treatments"""
        score_max = float(request.query_params.get('score_max', 5.0))
        ontology = OntologyQuery()
        traitements = ontology.get_traitements_eco_responsables(score_max)
        return Response(traitements)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        type_traitement = request.query_params.get('type')
        if type_traitement:
            traitements = Traitement.objects.filter(type_traitement=type_traitement)
            serializer = self.get_serializer(traitements, many=True)
            return Response(serializer.data)
        return Response({"error": "type parameter required"}, status=400)

class MedicamentViewSet(viewsets.ModelViewSet):
    queryset = Medicament.objects.all()
    serializer_class = MedicamentSerializer

class ImpactEnvironnementalViewSet(viewsets.ModelViewSet):
    queryset = ImpactEnvironnemental.objects.all()
    serializer_class = ImpactEnvironnementalSerializer
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        stats = ImpactEnvironnemental.objects.aggregate(
            score_moyen=Avg('score_carbone'),
            eau_moyenne=Avg('consommation_eau'),
            dechets_moyens=Avg('dechets'),
        )
        stats['nombre_recyclables'] = ImpactEnvironnemental.objects.filter(recyclable=True).count()
        stats['nombre_total'] = ImpactEnvironnemental.objects.count()
        return Response(stats)

class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

class DiagnosticViewSet(viewsets.ModelViewSet):
    queryset = Diagnostic.objects.all()
    serializer_class = DiagnosticSerializer
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        patient_id = request.query_params.get('patient_id')
        if patient_id:
            diagnostics = Diagnostic.objects.filter(patient_id=patient_id)
            serializer = self.get_serializer(diagnostics, many=True)
            return Response(serializer.data)
        return Response({"error": "patient_id required"}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_medecin(self, request):
        medecin_id = request.query_params.get('medecin_id')
        if medecin_id:
            diagnostics = Diagnostic.objects.filter(medecin_id=medecin_id)
            serializer = self.get_serializer(diagnostics, many=True)
            return Response(serializer.data)
        return Response({"error": "medecin_id required"}, status=400)

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    
    @action(detail=False, methods=['get'])
    def eco_alternatives(self, request):
        """Find eco-friendly prescription alternatives"""
        prescriptions = Prescription.objects.filter(
            traitement__impact_environnemental__score_carbone__lte=5
        ).select_related('traitement', 'diagnostic', 'traitement__impact_environnemental')
        serializer = self.get_serializer(prescriptions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def dashboard_stats(request):
    """Get overall dashboard statistics"""
    stats = {
        'patients': Patient.objects.count(),
        'medecins': Medecin.objects.count(),
        'maladies': Maladie.objects.count(),
        'traitements': Traitement.objects.count(),
        'diagnostics': Diagnostic.objects.count(),
        'prescriptions': Prescription.objects.count(),
        'etablissements': Etablissement.objects.count(),
        'examens': Examen.objects.count(),
        'traitements_eco': Traitement.objects.filter(
            impact_environnemental__score_carbone__lte=5
        ).count(),
        'impact_moyen': ImpactEnvironnemental.objects.aggregate(
            Avg('score_carbone')
        )['score_carbone__avg'] or 0,
    }
    return Response(stats)

@api_view(['GET'])
def ontology_query(request):
    """Execute custom SPARQL queries"""
    query_type = request.query_params.get('type', 'patients')
    ontology = OntologyQuery()
    
    if query_type == 'patients':
        results = ontology.get_all_patients()
    elif query_type == 'eco_traitements':
        score_max = float(request.query_params.get('score_max', 5.0))
        results = ontology.get_traitements_eco_responsables(score_max)
    elif query_type == 'medecins_specialite':
        specialite = request.query_params.get('specialite', 'Generaliste')
        results = ontology.get_medecins_by_specialite(specialite)
    else:
        return Response({"error": "Invalid query type"}, status=400)
    
    return Response(results)

@api_view(['GET'])
def semantic_alternatives(request):
    """
    SEMANTIC SEARCH: Find treatment alternatives using graph pattern matching.
    Compares all treatments for same disease automatically.
    """
    maladie_nom = request.query_params.get('maladie', 'Hypertension Artérielle')
    ontology = OntologyQuery()
    alternatives = ontology.get_treatment_alternatives_by_disease(maladie_nom)
    return Response(alternatives)

@api_view(['GET'])
def semantic_recommendation(request):
    """
    SEMANTIC SEARCH: Get intelligent treatment recommendations.
    Calculates eco-efficiency ratio (efficacy / environmental impact).
    """
    maladie_nom = request.query_params.get('maladie', 'Hypertension Artérielle')
    max_score = float(request.query_params.get('max_score', 10))
    ontology = OntologyQuery()
    recommendations = ontology.get_best_treatment_recommendation(maladie_nom, max_score)
    return Response(recommendations)

@api_view(['GET'])
def semantic_eco_doctors(request):
    """
    SEMANTIC SEARCH: Find experienced doctors who prescribe eco-friendly treatments.
    Multi-hop reasoning across doctor -> prescription -> treatment -> impact.
    """
    min_experience = int(request.query_params.get('min_experience', 5))
    max_impact = float(request.query_params.get('max_impact', 5))
    ontology = OntologyQuery()
    doctors = ontology.get_eco_conscious_doctors(min_experience, max_impact)
    return Response(doctors)