from django.contrib import admin
from .models import *

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom_etablissement', 'type_etablissement', 'capacite')
    list_filter = ('type_etablissement',)
    search_fields = ('nom_etablissement',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'numero_securite_sociale', 'groupe_sanguin', 'etablissement')
    list_filter = ('sexe', 'groupe_sanguin')
    search_fields = ('nom', 'prenom', 'email', 'numero_securite_sociale')
    date_hierarchy = 'date_naissance'

@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'specialite', 'numero_ordre', 'annees_experience', 'etablissement')
    list_filter = ('specialite',)
    search_fields = ('nom', 'prenom', 'email', 'numero_ordre')

@admin.register(Maladie)
class MaladieAdmin(admin.ModelAdmin):
    list_display = ('nom_maladie', 'type_maladie', 'gravite', 'contagieuse', 'code_cim10')
    list_filter = ('type_maladie', 'gravite', 'contagieuse')
    search_fields = ('nom_maladie', 'code_cim10')

@admin.register(Symptome)
class SymptomeAdmin(admin.ModelAdmin):
    list_display = ('nom_symptome', 'type_symptome', 'intensite', 'duree_symptome')
    list_filter = ('type_symptome', 'intensite')
    search_fields = ('nom_symptome',)

@admin.register(ImpactEnvironnemental)
class ImpactEnvironnementalAdmin(admin.ModelAdmin):
    list_display = ('type_impact', 'score_carbone', 'consommation_eau', 'dechets', 'recyclable')
    list_filter = ('type_impact', 'recyclable')

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom_medicament', 'type_medicament', 'dosage', 'forme', 'fabricant')
    list_filter = ('type_medicament', 'forme')
    search_fields = ('nom_medicament', 'fabricant')

@admin.register(Traitement)
class TraitementAdmin(admin.ModelAdmin):
    list_display = ('nom_traitement', 'type_traitement', 'maladie', 'cout', 'duree', 'efficacite')
    list_filter = ('type_traitement',)
    search_fields = ('nom_traitement',)
    raw_id_fields = ('maladie', 'impact_environnemental')
    filter_horizontal = ('medicaments',)

@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('nom_examen', 'type_examen', 'date_examen', 'cout_examen')
    list_filter = ('type_examen',)
    search_fields = ('nom_examen',)
    date_hierarchy = 'date_examen'

@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('patient', 'maladie', 'medecin', 'date_diagnostic')
    list_filter = ('date_diagnostic',)
    search_fields = ('patient__nom', 'patient__prenom', 'medecin__nom')
    raw_id_fields = ('patient', 'maladie', 'medecin')
    filter_horizontal = ('examens',)
    date_hierarchy = 'date_diagnostic'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('get_patient', 'traitement', 'duree_prescription', 'renouvellement', 'date_prescription')
    list_filter = ('renouvellement', 'date_prescription')
    search_fields = ('diagnostic__patient__nom', 'traitement__nom_traitement')
    raw_id_fields = ('diagnostic', 'traitement')
    date_hierarchy = 'date_prescription'
    
    def get_patient(self, obj):
        return f"{obj.diagnostic.patient.prenom} {obj.diagnostic.patient.nom}"
    get_patient.short_description = 'Patient'