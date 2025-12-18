import re

def compute_propensity_score(lead):
    """
    Assign a propensity to buy (0-100) based on weighted signals.
    Lead dict should have enrichment fields.
    """
    score = 0

    # Role Fit
    if re.search(r"toxicology|safety|hepatic|3d", lead.get("title", ""), re.I):
        score += 30

    # Scientific Intent
    if lead.get('recent_relevant_publication', False):
        score += 40

    # Company Intent
    if lead.get('recent_funding', False) or lead.get('major_grant', False):
        score += 20

    # Technographics
    if lead.get('uses_invitrio_or_nams', False):
        score += 15

    # Location
    if lead.get('location_major_hub', False):
        score += 10

    # Openness to NAMs
    if lead.get('mentions_nams', False):
        score += 10

    # Cap at 100
    return min(score, 100)

