practice3_order_2022 = {
    1: 'Bahrain',
    2: 'Saudi Arabia',
    3: 'Australia',
    4: 'Miami',
    5: 'Spain',
    6: 'Monaco',
    7: 'Azerbaijan',
    8: 'Canada',
    9: 'Great Britain',
    10: 'France',
    11: 'Hungary',
    12: 'Belgium',
    13: 'Netherlands',
    14: 'Italy',
    15: 'Singapore',
    16: 'Japan',
    17: 'United States',
    18: 'Mexico',
    19: 'Abu Dhabi'
}

practice3_order_2023 = {
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

practice3_order_2024 = {
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

practice3_orders = {
    2022: practice3_order_2022,
    2023: practice3_order_2023,
    2024: practice3_order_2024,
}

unique_practice3 = []
for practices3 in practice3_orders.values():
    for practice3 in practices3.values():
        if practice3 not in unique_practice3:
            unique_practice3.append(practice3)
unique_practice3.sort()