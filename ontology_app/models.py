from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Utilisateur(models.Model):
    """Classe parent pour Patient et Medecin"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=20, choices=[('M', 'Masculin'), ('F', 'Féminin'), ('A', 'Autre')], default='M')
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Etablissement(models.Model):
    """Établissement de santé"""
    TYPE_CHOICES = [
        ('hopital', 'Hôpital'),
        ('clinique', 'Clinique'),
        ('cabinet', 'Cabinet Médical'),
        ('pharmacie', 'Pharmacie'),
        ('laboratoire', 'Laboratoire'),
    ]
    
    nom_etablissement = models.CharField(max_length=200)
    adresse_etablissement = models.TextField()
    type_etablissement = models.CharField(max_length=20, choices=TYPE_CHOICES, default='hopital')
    capacite = models.IntegerField(default=0)
    certifications = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom_etablissement
    
    class Meta:
        verbose_name_plural = "Établissements"

class Patient(Utilisateur):
    """Patient recevant des soins"""
    numero_securite_sociale = models.CharField(max_length=15, unique=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    groupe_sanguin = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    
    class Meta:
        verbose_name_plural = "Patients"

class Medecin(Utilisateur):
    """Médecin prescrivant des traitements"""
    SPECIALITE_CHOICES = [
        ('generaliste', 'Généraliste'),
        ('cardiologue', 'Cardiologue'),
        ('pneumologue', 'Pneumologue'),
        ('autre', 'Autre spécialité'),
    ]
    
    numero_ordre = models.CharField(max_length=20, unique=True)
    specialite = models.CharField(max_length=50, choices=SPECIALITE_CHOICES)
    annees_experience = models.IntegerField(default=0)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True, related_name='medecins')
    
    class Meta:
        verbose_name_plural = "Médecins"

class Maladie(models.Model):
    """Pathologie ou condition médicale"""
    TYPE_CHOICES = [
        ('chronique', 'Maladie Chronique'),
        ('aigue', 'Maladie Aiguë'),
        ('infectieuse', 'Maladie Infectieuse'),
        ('cardiovasculaire', 'Maladie Cardiovasculaire'),
        ('respiratoire', 'Maladie Respiratoire'),
    ]
    
    nom_maladie = models.CharField(max_length=200, unique=True)
    code_cim10 = models.CharField(max_length=10, blank=True)
    type_maladie = models.CharField(max_length=30, choices=TYPE_CHOICES)
    gravite = models.CharField(max_length=20, choices=[('legere', 'Légère'), ('moderee', 'Modérée'), ('grave', 'Grave')])
    taux_mortalite = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    contagieuse = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom_maladie
    
    class Meta:
        verbose_name_plural = "Maladies"

class Symptome(models.Model):
    """Symptôme médical observable"""
    TYPE_CHOICES = [
        ('respiratoire', 'Symptôme Respiratoire'),
        ('digestif', 'Symptôme Digestif'),
        ('neurologique', 'Symptôme Neurologique'),
        ('douleur', 'Douleur'),
        ('fievre', 'Fièvre'),
    ]
    
    nom_symptome = models.CharField(max_length=200)
    type_symptome = models.CharField(max_length=30, choices=TYPE_CHOICES)
    intensite = models.CharField(max_length=20, choices=[('faible', 'Faible'), ('moderee', 'Modérée'), ('forte', 'Forte')])
    duree_symptome = models.IntegerField(help_text="Durée en jours")
    maladies = models.ManyToManyField(Maladie, related_name='symptomes', blank=True)
    
    def __str__(self):
        return self.nom_symptome
    
    class Meta:
        verbose_name_plural = "Symptômes"

class ImpactEnvironnemental(models.Model):
    """Impact environnemental d'un traitement"""
    TYPE_CHOICES = [
        ('faible', 'Impact Faible'),
        ('modere', 'Impact Modéré'),
        ('eleve', 'Impact Élevé'),
    ]
    
    type_impact = models.CharField(max_length=20, choices=TYPE_CHOICES)
    score_carbone = models.DecimalField(max_digits=10, decimal_places=2, help_text="Score en kg CO2")
    consommation_eau = models.DecimalField(max_digits=10, decimal_places=2, help_text="Consommation en litres")
    dechets = models.DecimalField(max_digits=10, decimal_places=2, help_text="Déchets en kg")
    recyclable = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.type_impact} - Score: {self.score_carbone}"
    
    class Meta:
        verbose_name = "Impact Environnemental"
        verbose_name_plural = "Impacts Environnementaux"
    
    def save(self, *args, **kwargs):
        # Auto-determine type based on score
        if self.score_carbone < 5:
            self.type_impact = 'faible'
        elif self.score_carbone <= 15:
            self.type_impact = 'modere'
        else:
            self.type_impact = 'eleve'
        super().save(*args, **kwargs)

class Medicament(models.Model):
    """Médicament utilisé dans un traitement"""
    TYPE_CHOICES = [
        ('antibiotique', 'Antibiotique'),
        ('anti_inflammatoire', 'Anti-inflammatoire'),
        ('analgesique', 'Analgésique'),
        ('antiviral', 'Antiviral'),
        ('anticoagulant', 'Anticoagulant'),
    ]
    
    nom_medicament = models.CharField(max_length=200, unique=True)
    type_medicament = models.CharField(max_length=30, choices=TYPE_CHOICES)
    dosage = models.CharField(max_length=100)
    forme = models.CharField(max_length=50, help_text="Comprimé, sirop, injection, etc.")
    fabricant = models.CharField(max_length=200)
    effets_secondaires = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nom_medicament} ({self.dosage})"
    
    class Meta:
        verbose_name_plural = "Médicaments"

class Traitement(models.Model):
    """Traitement médical prescrit"""
    TYPE_CHOICES = [
        ('medicamenteux', 'Traitement Médicamenteux'),
        ('chirurgie', 'Chirurgie'),
        ('physiotherapie', 'Physiothérapie'),
        ('radiotherapie', 'Radiothérapie'),
        ('psychotherapie', 'Psychothérapie'),
    ]
    
    nom_traitement = models.CharField(max_length=200)
    type_traitement = models.CharField(max_length=30, choices=TYPE_CHOICES)
    cout = models.DecimalField(max_digits=10, decimal_places=2, help_text="Coût en euros")
    duree = models.IntegerField(help_text="Durée en jours")
    efficacite = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Efficacité en %")
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    # Relations
    maladie = models.ForeignKey(Maladie, on_delete=models.CASCADE, related_name='traitements')
    medicaments = models.ManyToManyField(Medicament, blank=True, related_name='traitements')
    impact_environnemental = models.OneToOneField(ImpactEnvironnemental, on_delete=models.CASCADE, null=True, blank=True, related_name='traitement')
    
    def __str__(self):
        return f"{self.nom_traitement} pour {self.maladie.nom_maladie}"
    
    class Meta:
        verbose_name_plural = "Traitements"

class Examen(models.Model):
    """Examen médical ou diagnostic"""
    TYPE_CHOICES = [
        ('biologique', 'Examen Biologique'),
        ('imagerie', 'Examen d\'Imagerie'),
        ('clinique', 'Examen Clinique'),
        ('fonctionnel', 'Examen Fonctionnel'),
    ]
    
    nom_examen = models.CharField(max_length=200)
    type_examen = models.CharField(max_length=30, choices=TYPE_CHOICES)
    date_examen = models.DateField()
    resultat = models.TextField(blank=True)
    cout_examen = models.DecimalField(max_digits=10, decimal_places=2)
    maladies_diagnostiquees = models.ManyToManyField(Maladie, blank=True, related_name='examens')
    
    def __str__(self):
        return f"{self.nom_examen} - {self.date_examen}"
    
    class Meta:
        verbose_name_plural = "Examens"

class Diagnostic(models.Model):
    """Relation entre Patient, Maladie et Médecin"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnostics')
    maladie = models.ForeignKey(Maladie, on_delete=models.CASCADE, related_name='diagnostics')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='diagnostics')
    date_diagnostic = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    examens = models.ManyToManyField(Examen, blank=True, related_name='diagnostics')
    
    class Meta:
        verbose_name_plural = "Diagnostics"
        ordering = ['-date_diagnostic']
    
    def __str__(self):
        return f"{self.patient} - {self.maladie.nom_maladie}"

class Prescription(models.Model):
    """Prescription de traitement pour un diagnostic"""
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, related_name='prescriptions')
    traitement = models.ForeignKey(Traitement, on_delete=models.CASCADE, related_name='prescriptions')
    date_prescription = models.DateTimeField(auto_now_add=True)
    posologie = models.TextField(help_text="Instructions de prise")
    duree_prescription = models.IntegerField(help_text="Durée en jours")
    renouvellement = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Prescriptions"
        ordering = ['-date_prescription']
    
    def __str__(self):
        return f"{self.traitement.nom_traitement} pour {self.diagnostic.patient}"