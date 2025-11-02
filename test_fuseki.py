# test_fuseki.py
import requests

print("=" * 60)
print("TESTING FUSEKI CONNECTION")
print("=" * 60)

# Test 1: Is Fuseki running?
print("\n1️⃣  Testing if Fuseki is running...")
try:
    response = requests.get('http://localhost:3030', timeout=5)
    print(f"   ✅ Fuseki is running (HTTP {response.status_code})")
except Exception as e:
    print(f"   ❌ Cannot connect to Fuseki: {e}")
    print("   💡 Start Fuseki with: fuseki-server")
    exit(1)

# Test 2: Does the dataset exist?
print("\n2️⃣  Testing if 'health_env' dataset exists...")
try:
    response = requests.get('http://localhost:3030/$/datasets', timeout=5)
    if 'health_env' in response.text:
        print("   ✅ Dataset 'health_env' exists")
    else:
        print("   ❌ Dataset 'health_env' NOT FOUND")
        print("   💡 Create it at: http://localhost:3030")
        exit(1)
except Exception as e:
    print(f"   ❌ Error checking datasets: {e}")
    exit(1)

# Test 3: Can we query?
print("\n3️⃣  Testing SPARQL query...")
query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
try:
    response = requests.get(
        'http://localhost:3030/health_env/query',
        params={'query': query},
        headers={'Accept': 'application/sparql-results+json'},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        count = data['results']['bindings'][0]['count']['value']
        print(f"   ✅ Query successful! Found {count} triples")
        if count == '0':
            print("   ⚠️  No data in Fuseki yet - upload your OWL file first")
    else:
        print(f"   ❌ Query failed (HTTP {response.status_code})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Can we insert?
print("\n4️⃣  Testing SPARQL insert...")
test_query = """
PREFIX health: <http://example.org/health#>
INSERT DATA { 
    health:TestPatient_999 a health:Patient ;
        health:nom "Test" ;
        health:prenom "User" .
}
"""
try:
    response = requests.post(
        'http://localhost:3030/health_env/update',
        data={'update': test_query},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=5
    )
    if response.status_code == 204:
        print("   ✅ Insert successful!")
        
        # Clean up test data
        cleanup = "PREFIX health: <http://example.org/health#> DELETE WHERE { health:TestPatient_999 ?p ?o }"
        requests.post('http://localhost:3030/health_env/update', 
                     data={'update': cleanup},
                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
    else:
        print(f"   ❌ Insert failed (HTTP {response.status_code})")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - You can now run populate_fuseki.py")
print("=" * 60)