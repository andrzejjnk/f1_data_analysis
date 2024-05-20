practice2_order_2022 = {
    1: 'Bahrain',
    2: 'Saudi Arabia',
    3: 'Australia',
    4: 'Imola',
    5: 'Miami',
    6: 'Spain',
    7: 'Monaco',
    8: 'Azerbaijan',
    9: 'Canada',
    10: 'Great Britain',
    11: 'Austria',
    12: 'France',
    13: 'Hungary',
    14: 'Belgium',
    15: 'Netherlands',
    16: 'Italy',
    17: 'Singapore',
    18: 'Japan',
    19: 'United States',
    20: 'Mexico',
    21: 'Brazil',
    22: 'Abu Dhabi'
}

practice2_order_2023 = {
    1: 'Bahrain',
    2: 'Saudi Arabia',
    3: 'Australia',
    4: 'Miami',
    5: 'Monaco',
    6: 'Spain',
    7: 'Canada',
    8: 'Great Britain',
    9: 'Hungary',
    10: 'Netherlands',
    11: 'Italy',
    12: 'Singapore',
    13: 'Japan',
    14: 'Mexico',
    15: 'Las Vegas',
    16: 'Abu Dhabi'
}

practice2_order_2024 = {
    1: 'Bahrain',
    2: 'Saudi Arabia',
    3: 'Australia',
    4: 'Japan',
    # 5: 'China' # to delete because it's sprint weekend
    # 6: 'Miami', # to delete because it's sprint weekend
    5: 'Imola'
    # 8: 'Monaco',
    # 9: 'Canada',
    # 10: 'Spain',
    # 11: 'Austria',
    # 12: 'Great Britain',
    # 13: 'Hungary',
    # 14: 'Belgium',
    # 15: 'Netherlands',
    # 16: 'Italy',
    # 17: 'Azerbaijan',
    # 18: 'Singapore',
    # 19: 'United States',
    # 20: 'Mexico',
    # 21: 'Brazil',
    # 22: 'Las Vegas',
    # 23: 'Qatar',
    # 24: 'Abu Dhabi'
}

practice2_orders = {
    2022: practice2_order_2022,
    2023: practice2_order_2023,
    2024: practice2_order_2024,
}

unique_practice2 = []
for practices2 in practice2_orders.values():
    for practice2 in practices2.values():
        if practice2 not in unique_practice2:
            unique_practice2.append(practice2)
unique_practice2.sort()