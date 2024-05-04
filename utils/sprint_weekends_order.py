sprint_order_2022 = {
    1: 'Austria',
    2: 'Imola',
    3: 'Brazil'
}

sprint_order_2023 = {
    1: 'Azerbaijan',
    2: 'Austria',
    3: 'Belgium',
    4: 'Qatar',
    5: 'United States',
    6: 'Brazil'
}

sprint_order_2024 = {
    1: 'China'
    # 2: 'Miami',
    # 3: 'Austria',
    # 4: 'United States',
    # 5: 'Brazil',
    # 6: 'Qatar'
}

sprint_orders = {
    2022: sprint_order_2022,
    2023: sprint_order_2023,
    2024: sprint_order_2024,
}

unique_sprints = []
for sprints in sprint_orders.values():
    for sprint in sprints.values():
        if sprint not in unique_sprints:
            unique_sprints.append(sprint)
unique_sprints.sort()
