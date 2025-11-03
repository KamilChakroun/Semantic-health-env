# 🏥 Semantic Health Env

**Intelligent Healthcare Decision Support System Integrating Clinical Efficacy with Environmental Sustainability**

A cutting-edge web application that blends **Semantic Web technologies** (OWL ontologies, SPARQL) with **relational databases** to help healthcare professionals make **eco-responsible treatment decisions** without compromising **clinical performance**.

---

## 🧩 Overview

Semantic Health Env allows hospitals and researchers to:

* ⚕️ Compare treatments for the same disease based on both **clinical efficacy** and **environmental impact**.
* 🌱 Recommend **eco-efficient** alternatives using **semantic reasoning**.
* 🧠 Bridge **traditional databases** (PostgreSQL) with **semantic triple stores** (Apache Jena Fuseki).

---

## 🌟 Key Features

### 🔮 Semantic Reasoning

* **Treatment Alternatives:** Compare all treatments for a disease using SPARQL graph matching.
* **Eco-Efficiency Ratios:** Compute `efficacy ÷ carbon impact` to find optimal trade-offs.
* **Multi-Hop Reasoning:** Explore complex relationships across patients, diseases, and treatments.

### 💚 Environmental Sustainability

* Track **carbon footprint**, **water usage**, and **waste generation** per treatment.
* Identify **recyclable vs. non-recyclable** options.
* Filter eco-friendly alternatives (impact score < 5 kg CO₂).

### 🏥 Clinical Management

* Manage **patients**, **doctors**, and **diseases** in one platform.
* Track **diagnoses**, **prescriptions**, and **statistics**.
* Supports **multi-establishment operations**.

### 🎨 User Interface

* Modern, responsive dashboard with gradient themes.
* Real-time data visualizations.
* Side-by-side source comparison: **PostgreSQL vs. SPARQL**.

---

## 🏗️ Architecture

```bash
Frontend (HTML / CSS / JS)
│
│  REST API (JSON)
│
↓
Django Backend (Python)
 ├── Models aligned with OWL ontology
 ├── REST endpoints (DRF)
 └── SPARQL integration
│
├── PostgreSQL → Fast CRUD operations
└── Apache Jena Fuseki → Semantic reasoning & inference
```

**Hybrid Benefit:**
⚡ PostgreSQL for standard ops · 🧠 Fuseki for intelligent reasoning · 🔄 Seamless switching between sources

---

## 📦 Installation

### 🔧 Prerequisites

* Python 3.8+
* PostgreSQL 12+ *(or SQLite for dev)*
* Apache Jena Fuseki
* Java 11+ *(for Fuseki)*

### ⚙️ Setup

```bash
# 1️⃣ Clone repository
git clone https://github.com/yourusername/Semantic-Health-Env.git
cd Semantic-Health-Env

# 2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run migrations & create admin
python manage.py migrate
python manage.py createsuperuser

# 5️⃣ Populate database with demo data
python populate_database.py
```

### 🧠 Setup Fuseki (Optional)

```bash
cd path\to\apache-jena-fuseki
mkdir databases
fuseki-server.bat --update --loc=databases/health_env /health_env
```

Upload your ontology at
➡️ `http://localhost:3030/` → **manage datasets** → *health_env* → *upload files*

Then:

```bash
python populate_fuseki.py
```

---

## 🚀 Run the App

```bash
# Start Django server
python manage.py runserver
```

Access the app:

| Service  | URL                                                        | Description      |
| -------- | ---------------------------------------------------------- | ---------------- |
| Frontend | [http://localhost:8000](http://localhost:8000)             | Main Interface   |
| Admin    | [http://localhost:8000/admin](http://localhost:8000/admin) | Django Admin     |
| API Root | [http://localhost:8000/api/](http://localhost:8000/api/)   | REST API         |
| Fuseki   | [http://localhost:3030](http://localhost:3030)             | SPARQL Interface |

---

## 🌱 Example: Eco-Friendly Treatment Search

* Go to **🌿 Éco-responsable** tab
* Set carbon score threshold (e.g., < 5.0 kg CO₂)
* Choose data source:

  * ⚡ PostgreSQL → fast relational query
  * 🔮 SPARQL → semantic reasoning

**Result:** side-by-side comparison of eco-friendly treatment options.

---

## 🔬 Technology Stack

### Backend

* **Django 4.2.7** — Web framework
* **Django REST Framework** — REST API
* **PostgreSQL / SQLite** — Database
* **SPARQLWrapper + RDFLib** — Semantic data interaction

### Frontend

* **HTML5 / CSS3 / Vanilla JS** — Responsive UI
* **Chart.js / Custom JS** — Real-time visualization

### Semantic Layer

* **OWL Ontology** — Domain model
* **Apache Jena Fuseki** — SPARQL endpoint
* **SPARQL 1.1** — Query language

---

## 📊 Sample Data

| Entity         | Count | Description              |
| -------------- | ----- | ------------------------ |
| Establishments | 3     | Hospital, Clinic, Office |
| Doctors        | 5     | Various specialties      |
| Patients       | 4     | Full profiles            |
| Diseases       | 6     | Chronic & acute          |
| Treatments     | 13    | Range of impacts         |
| Medications    | 5     | Linked to treatments     |

**Example:**
*Hypertension* has 5 treatment options ranging from
🌿 0.8 kg CO₂ → 💊 25.3 kg CO₂ (94% efficacy).

---

## 🎯 API Endpoints

```http
GET  /api/patients/                       # List patients
GET  /api/traitements/eco_responsables/   # Eco-friendly (SQL)
GET  /api/traitements/eco_ontology/       # Eco-friendly (SPARQL)
GET  /api/semantic/alternatives/?maladie=Hypertension
GET  /api/semantic/recommendation/?maladie=Diabète
GET  /api/stats/                          # Statistics
```

---

## 🧠 Educational Value

This project demonstrates:

* **Semantic Web Integration** → OWL, RDF, SPARQL reasoning
* **Full-Stack Engineering** → Django + REST + Semantic layer
* **Decision Support Modeling** → Merging sustainability and clinical data
* **Hybrid Architecture Thinking** → Choosing relational vs. semantic data

---

## 🧩 Project Structure

```bash
Semantic-Health-Env/
├── health_environment/          # Django project config
├── ontology_app/                # Main app (models, views, SPARQL)
├── ontology_health_environment.owl
├── populate_database.py
├── populate_fuseki.py
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Configuration (.env)

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=health_env_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

FUSEKI_ENDPOINT=http://localhost:3030/health_env/sparql
FUSEKI_UPDATE_ENDPOINT=http://localhost:3030/health_env/update
```

---

## 🧩 Use Cases

1. 🏥 **Hospital Decision Support:** Choose treatments balancing efficacy & sustainability.
2. 📚 **Research & Education:** Demonstrate semantic web applications in healthcare.
3. 🌍 **Environmental Policy:** Provide data-driven sustainability insights.
4. 👩‍⚕️ **Medical Training:** Train students on data-driven eco-healthcare.

---

## 🪛 Troubleshooting

| Issue                 | Solution                                                  |
| --------------------- | --------------------------------------------------------- |
| Fuseki not connecting | Ensure it's running at `http://localhost:3030/health_env` |
| Empty SPARQL results  | Run `python populate_fuseki.py`                           |
| DB migration errors   | Run `python manage.py migrate`                            |
| Import errors         | Activate venv & reinstall deps                            |

---

## 📚 Resources

* [Django Documentation](https://docs.djangoproject.com/)
* [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/)
* [SPARQL 1.1 Spec](https://www.w3.org/TR/sparql11-query/)
* [OWL Ontology Guide](https://www.w3.org/OWL/)
* [RDF Primer](https://www.w3.org/TR/rdf11-primer/)

---

<div align="center">

⭐ **Star this repo if you support sustainable healthcare!**
Made with ❤️ using Django, SPARQL, and Semantic Web technologies.

</div>
