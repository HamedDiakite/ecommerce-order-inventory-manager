# state_tax_rates.py

"""
Comprehensive US State Tax Rates for E-Commerce Transactions
-------------------------------------------------------------
This module contains sales tax rates for all 50 US states plus DC.

Tax rates are based on state-level sales tax only (not including local/county taxes).
Rates are approximate and should be verified for production use.

Last Updated: December 1, 2025
"""

# Dictionary mapping state codes to their sales tax rates (as decimals)
STATE_TAX_RATES = {
    # States with no sales tax
    "AK": 0.0000,  # Alaska - No state sales tax
    "DE": 0.0000,  # Delaware - No state sales tax
    "MT": 0.0000,  # Montana - No state sales tax
    "NH": 0.0000,  # New Hampshire - No state sales tax
    "OR": 0.0000,  # Oregon - No state sales tax
    
    # States with sales tax (sorted alphabetically)
    "AL": 0.0400,  # Alabama - 4%
    "AR": 0.0650,  # Arkansas - 6.5%
    "AZ": 0.0560,  # Arizona - 5.6%
    "CA": 0.0725,  # California - 7.25%
    "CO": 0.0290,  # Colorado - 2.9%
    "CT": 0.0635,  # Connecticut - 6.35%
    "DC": 0.0600,  # District of Columbia - 6%
    "FL": 0.0600,  # Florida - 6%
    "GA": 0.0400,  # Georgia - 4%
    "HI": 0.0400,  # Hawaii - 4%
    "IA": 0.0600,  # Iowa - 6%
    "ID": 0.0600,  # Idaho - 6%
    "IL": 0.0625,  # Illinois - 6.25%
    "IN": 0.0700,  # Indiana - 7%
    "KS": 0.0650,  # Kansas - 6.5%
    "KY": 0.0600,  # Kentucky - 6%
    "LA": 0.0445,  # Louisiana - 4.45%
    "MA": 0.0625,  # Massachusetts - 6.25%
    "MD": 0.0600,  # Maryland - 6%
    "ME": 0.0550,  # Maine - 5.5%
    "MI": 0.0600,  # Michigan - 6%
    "MN": 0.0688,  # Minnesota - 6.875%
    "MO": 0.0423,  # Missouri - 4.225%
    "MS": 0.0700,  # Mississippi - 7%
    "NC": 0.0475,  # North Carolina - 4.75%
    "ND": 0.0500,  # North Dakota - 5%
    "NE": 0.0550,  # Nebraska - 5.5%
    "NJ": 0.0663,  # New Jersey - 6.625%
    "NM": 0.0513,  # New Mexico - 5.125%
    "NV": 0.0685,  # Nevada - 6.85%
    "NY": 0.0400,  # New York - 4%
    "OH": 0.0575,  # Ohio - 5.75%
    "OK": 0.0450,  # Oklahoma - 4.5%
    "PA": 0.0600,  # Pennsylvania - 6%
    "RI": 0.0700,  # Rhode Island - 7%
    "SC": 0.0600,  # South Carolina - 6%
    "SD": 0.0450,  # South Dakota - 4.5%
    "TN": 0.0700,  # Tennessee - 7%
    "TX": 0.0625,  # Texas - 6.25%
    "UT": 0.0610,  # Utah - 6.1%
    "VA": 0.0530,  # Virginia - 5.3%
    "VT": 0.0600,  # Vermont - 6%
    "WA": 0.0650,  # Washington - 6.5%
    "WI": 0.0500,  # Wisconsin - 5%
    "WV": 0.0600,  # West Virginia - 6%
    "WY": 0.0400,  # Wyoming - 4%
}

# List of all state codes (useful for dropdowns/validation)
STATE_CODES = sorted(STATE_TAX_RATES.keys())

# Full state names mapped to state codes
STATE_NAMES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

# Formatted state list for display (e.g., "AL - Alabama")
STATE_DISPLAY_LIST = [f"{code} - {name}" for code, name in sorted(STATE_NAMES.items())]


def get_tax_rate(state_code):
    """
    Get the tax rate for a given state code.
    
    Args:
        state_code (str): Two-letter state code (e.g., "CA", "NY")
    
    Returns:
        float: Tax rate as a decimal (e.g., 0.0725 for 7.25%)
        Returns 0.0 if state code is invalid.
    """
    if not state_code:
        return 0.0
    
    state_code = state_code.strip().upper()
    return STATE_TAX_RATES.get(state_code, 0.0)


def is_valid_state(state_code):
    """
    Check if a state code is valid.
    
    Args:
        state_code (str): Two-letter state code
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not state_code:
        return False
    
    return state_code.strip().upper() in STATE_TAX_RATES


def get_state_name(state_code):
    """
    Get the full name of a state from its code.
    
    Args:
        state_code (str): Two-letter state code
    
    Returns:
        str: Full state name, or "Unknown" if invalid
    """
    if not state_code:
        return "Unknown"
    
    return STATE_NAMES.get(state_code.strip().upper(), "Unknown")


def calculate_tax(subtotal, state_code):
    """
    Calculate tax amount for a given subtotal and state.
    
    Args:
        subtotal (float): Subtotal amount before tax
        state_code (str): Two-letter state code
    
    Returns:
        tuple: (tax_amount, total_with_tax)
    """
    tax_rate = get_tax_rate(state_code)
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    return tax_amount, total
