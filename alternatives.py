alternatives = {
    "burger": ["chapati", "dhokla", "idli"],
    "pizza": ["masala_dosa", "dhokla", "idli"],
    "samosa": ["dhokla", "idli", "chapati"],
    "jalebi": ["idli", "dhokla", "chapati"],
    "pakode": ["dhokla", "idli", "chapati"],
    "chole_bhature": ["chapati", "idli", "dhokla"],
    "fried_rice": ["chapati", "idli", "dhokla"],
    "paani_puri": ["dhokla", "idli", "chapati"]
}

def get_alternatives(food):
    return alternatives.get(food, [])