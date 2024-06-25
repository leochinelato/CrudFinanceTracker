from datetime import datetime


def transform_dot_in_comma(float_number):
    return f"{float_number:.2f}".replace(".", ",")


def get_greeting(name):
    current_hour = datetime.now().hour

    if current_hour < 12:
        return f"Bom dia, {name}."
    elif 12 <= current_hour < 18:
        return f"Boa tarde, {name}."
    return f"Boa noite, {name}."
