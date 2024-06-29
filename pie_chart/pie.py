import plotly.express as px
import plotly.io as pio


def categories_and_values(transactions, categories):
    category_sums = {
        category['name']: 0
        for category in categories
    }

    for transaction in transactions:
        if transaction['type'] == 'expense':
            value = float(transaction['value'].replace(",", "."))
            category_name = transaction['category']
            category_sums[category_name] += value

    filtered_expenses = {k: v for k, v in category_sums.items() if v > 0}

    categories_plot = list(filtered_expenses.keys())
    values_plot = list(filtered_expenses.values())

    total = sum(values_plot)

    percentages = [
        (valor / total) * 100 if total > 0 else 0
        for valor in values_plot
    ]

    return categories_plot, values_plot, percentages
