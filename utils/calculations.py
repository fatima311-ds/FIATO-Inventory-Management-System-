def convert_to_base_unit(quantity, from_unit, base_unit):

    if from_unit == base_unit:
        return quantity

    conversions = {
        ("kg", "g"): 1000,
        ("g", "kg"): 0.001,
        ("L", "ml"): 1000,
        ("ml", "L"): 0.001,
    }

    key = (from_unit, base_unit)

    if key not in conversions:
        raise ValueError(
            f"Cannot convert {from_unit} to {base_unit}"
        )

    return quantity * conversions[key]
def get_base_unit(unit):

    unit = unit.lower().strip()

    if unit in ["kg", "g"]:
        return "g"

    if unit in ["l", "ml"]:
        return "ml"

    raise ValueError(f"Unsupported unit: {unit}")