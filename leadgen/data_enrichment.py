import random

def enrich_lead(lead):
    """
    Take base profile and return enriched lead dict (mock enrichment example).
    """
    # Map company HQs and major hubs
    company_hq_map = {
        'BioSynth Pharma': 'Basel, Switzerland',
        'MedInnovate Inc.': 'Cambridge, MA',
        'GenPro Biologics': 'San Diego, CA',
        'Cambridge 3D Organoids': 'Cambridge, UK',
        'Astra Therapeutics': 'Boston, MA',
        'StartBioX': 'Austin, TX',
        'CoreTox Labs': 'Berlin, Germany',
        'AltTox Solutions': 'San Francisco, CA',
        'LiverOrganoTech': 'Boston, MA',
        'GlobalCRO Partners': 'Basel, Switzerland',
        'AltBiome Labs': 'London, UK',
        'NewCell Therapeutics': 'Cambridge, MA',
        'MiniLab Genomics': 'Oxford, UK',
        'InnoVito 3D': 'Basel, Switzerland',
        'SafeTox AG': 'Basel, Switzerland'
    }
    major_hubs = ["Boston", "Cambridge", "Basel", "San Francisco", "Bay Area", "UK"]

    email = f"{lead['name'].split()[1].lower()}@{lead['company'].replace(' ', '').lower()}.com" if ' ' in lead['name'] else "info@company.com"
    hq = company_hq_map.get(lead["company"], "Unknown")
    location = random.choice([hq, "Remote", "".join([random.choice(major_hubs), ", USA"]), "HQ" if random.random()>0.5 else "Remote"])
    size_sector = random.choice([
        ("Mid-size", "Biotech"),
        ("Enterprise", "Big Pharma"),
        ("Small", "Startup"),
        ("Large", "CRO")
    ])

    # Mock scientific/market signals
    recent_pub = random.random() > 0.33
    recent_pub_kw = recent_pub and random.choice([
        "Drug-Induced Liver Injury (DILI)", "3D cell culture", "Hepatic spheroids", "Organ-on-chip", "Investigative toxicology", "General"
    ]) or None
    funding = random.random() > 0.7
    grant = not funding and random.random()>0.7
    partnerships = random.random()>0.7
    uses_nams = random.random()>0.7 or "NAM" in lead["title"].upper()
    mentions_nams = "nams" in (lead["title"]+lead["company"]).lower() or uses_nams
    location_major_hub = any(hub.lower() in str(location).lower() for hub in major_hubs)

    return {
        **lead,
        "business_email": email,
        "company_hq": hq,
        "person_location": location,
        "company_size": size_sector[0],
        "company_sector": size_sector[1],
        "recent_relevant_publication": bool(recent_pub_kw and recent_pub_kw != "General"),
        "recent_publication_keywords": recent_pub_kw,
        "conference_speaker": random.random() > 0.8,
        "recent_funding": funding,
        "major_grant": grant,
        "recent_partnership": partnerships,
        "uses_invitrio_or_nams": uses_nams,
        "mentions_nams": mentions_nams,
        "location_major_hub": location_major_hub
    }

