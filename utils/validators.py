def validate_positive_number(value, field_name):

    if value is None:
        raise ValueError(f"{field_name} is required.")

    if value <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return True
def validate_non_negative(value, field_name):

    if value is None:
        raise ValueError(f"{field_name} is required.")

    if value < 0:
        raise ValueError(
            f"{field_name} cannot be negative."
        )

    return True