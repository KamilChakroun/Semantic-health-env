from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'etablissements', views.EtablissementViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'medecins', views.MedecinViewSet)
router.register(r'maladies', views.MaladieViewSet)
router.register(r'symptomes', views.SymptomeViewSet)
router.register(r'traitements', views.TraitementViewSet)
router.register(r'medicaments', views.MedicamentViewSet)
router.register(r'impacts', views.ImpactEnvironnementalViewSet)
router.register(r'examens', views.ExamenViewSet)
router.register(r'diagnostics', views.DiagnosticViewSet)
router.register(r'prescriptions', views.PrescriptionViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('api/ontology/query/', views.ontology_query, name='ontology-query'),
    path('api/semantic/alternatives/', views.semantic_alternatives, name='semantic-alternatives'),
    path('api/semantic/recommendation/', views.semantic_recommendation, name='semantic-recommendation'),
    path('api/semantic/eco-doctors/', views.semantic_eco_doctors, name='semantic-eco-doctors'),
]