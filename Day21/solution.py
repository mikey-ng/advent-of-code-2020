"""
Each allergen is in a single ingredient
For each allergen listed, the food that contains it must be included in the list of ingredients for each food that lists the allergen
To find the ingredient, determine the intersection of all ingredient lists that contain the allergen 

ex.
food1: ingred1 ingred2 ingred3 (contains allergen1)
food2: ingred1 ingred3 ingred4 (contains allergen1, allergen2)

ingred3 cannot be the source of allergen1 because allergen1 appears in food2 but ingred3 does not
possible sources of allergen1 are ingred1 and ingred2 since they are in all foods that allergen1 is found in
"""


import re
from collections import defaultdict
f = open('input')

ingredient_pattern = '.*(?= \()'
allergen_pattern = '(?<=\(contains )(.*)(?=\))'

allergens_map = {}
ingredient_count = defaultdict(int)
for line in f.read().split('\n'):
    ingredients = set(re.search(ingredient_pattern, line).group().split(' '))
    allergens = re.search(allergen_pattern, line).group().split(', ')

    # intersect ingredient lists for each food and allergen
    for allergen in allergens:
        if allergen not in allergens_map:
            allergens_map[allergen] = ingredients
        else:
            allergens_map[allergen] = allergens_map[allergen].intersection(ingredients)

    for ingredient in ingredients:
        ingredient_count[ingredient] += 1

# ingredients not found in any intersection are allergen-free 
ingredient_set = set(ingredient_count.keys())
for ingredients in allergens_map.values():
    ingredient_set -= ingredients

no_allergen_count = 0
for ingredient in ingredient_set:
    no_allergen_count += ingredient_count[ingredient]

print(no_allergen_count)

identified_allergens = {}
while len(allergens_map) > 0:

    # determine allegens with only a single ingredient
    identifiable_allergens = [allergen for allergen in allergens_map if len(allergens_map[allergen]) == 1]

    # move identified allergen/ingredient from allergens_map to identified_allergens
    for identifiable_allergen in identifiable_allergens:      
        ingredient = next(iter(allergens_map[identifiable_allergen]))
        identified_allergens[identifiable_allergen] = ingredient
        del allergens_map[identifiable_allergen]

        for allergen in allergens_map:
            if ingredient in allergens_map[allergen]:
                allergens_map[allergen].remove(ingredient)

# print ingredients sorted by allergen
ingredient_list = []
for allergen in sorted(identified_allergens.keys()):
    ingredient_list.append(identified_allergens[allergen])
print(','.join(ingredient_list))