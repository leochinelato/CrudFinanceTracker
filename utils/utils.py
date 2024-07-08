from datetime import datetime


def transform_dot_in_comma(float_number):
    return f"{float_number:.2f}".replace(".", ",")


def get_greeting():
    current_hour = datetime.now().hour

    if current_hour < 12:
        return f"Bom dia,"
    elif 12 <= current_hour < 18:
        return f"Boa tarde,"
    return f"Boa noite,"


# [{'id': 1, 'description': 'Air Jordan 1', 'value': '1200,00', 'date': '29/06/2024', 'type': 'expense', 'category': 'Gasto Desnecessário'}]
