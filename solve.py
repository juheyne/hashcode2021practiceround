import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs='+')
args = parser.parse_args()
print(args.file)


def read_file(file):
    with open(file) as f:
        _, t2, t3, t4 = f.readline().split()

        print(f"T2: {t2}, T3: {t3}, T4: {t4}")

        pizzas = dict()
        for pizza, line in enumerate(f):
            ingredients = line.split()[1:]
            pizzas[pizza] = ingredients

        # print(pizzas)
        return int(t2), int(t3), int(t4), pizzas


def output_file(file, deliveries):
    with open(file, "w+") as f:
        f.write(f"{str(len(deliveries))}\n")
        for delivery in deliveries:
            f.writelines(f"{len(delivery)} {' '.join(str(n) for n in delivery)}\n")


def find_unique_pizzas(pizzas):
    """
    Sort and count the pizzas based on their toppings

    :param pizzas: dict of pizza ids mapped list of toppings
    :return: unique pizzas: dict with tuple of toppings as keys and list of pizza ids as value
    """
    unique_pizzas = dict()

    for pizza_id, toppings_as_list in pizzas.items():
        toppings = tuple(set(toppings_as_list))  # Convert first to set to order toppings and hashable tuple
        if toppings in unique_pizzas:
            unique_pizzas[toppings].append(pizza_id)
        else:
            unique_pizzas[toppings] = [pizza_id]
    return unique_pizzas


def find_best_match(set_of_ingredient, dict_ingredient_tuple_to_ids):
    """
    Finds best match to given set of ingredients

    :param set_of_ingredient: set of ingredients to check for
    :param dict_ingredient_tuple_to_ids: dict with ingredient tuple matching ids
    :return: most_matching_id: one of the the id's with the best matching set from the dict
    :return: matched_set: toppings of best matching set and passed set_of_ingredients
    """
    most_matching_count = -1
    most_matching_id = -1
    matched_set = set()
    for key, value in dict_ingredient_tuple_to_ids.items():
        new_set = set_of_ingredient.union(set(key))
        if len(new_set) > most_matching_count:
            most_matching_count = len(new_set)
            most_matching_id = value[0]
            matched_set = key
    return most_matching_id, matched_set


def remove_pizza_id(pizzas, id):
    pizzas = {toppings: ids.remove(id) for toppings, ids in pizzas.items()}  # remove id from list
    pizzas = {toppings: ids for toppings, ids in pizzas.items() if not ids}
    return pizzas


def deliver_to_team(sorted_pizzas, team_size):
    """
    Combines pizza to deliver to team of given size. Only call if enough pizzas are left
    :param sorted_pizzas: dict of toppings to list of ids
    :param team_size: 2-4
    :return:
    """
    # Select first pizza of most rare topping set
    topping, pizza_ids = next(iter(sorted_pizzas.items()))
    # print("topping: ", topping, " ids: ", pizza_ids)
    pizza_id = pizza_ids[0]
    sorted_pizzas[topping].remove(pizza_id)
    if not sorted_pizzas[topping]:
        del sorted_pizzas[topping]

    # print("sorted_pizzas: ", sorted_pizzas)

    delivery = [pizza_id]

    # Feed team
    for _ in range(team_size-1):
        # Find until team is satisfied
        # Find 2nd pizza
        matched_id, matched_set = find_best_match(set(topping), sorted_pizzas)
        delivery.append(matched_id)
        sorted_pizzas[tuple(matched_set)].remove(matched_id)
        if not sorted_pizzas[tuple(matched_set)]:
            del sorted_pizzas[tuple(matched_set)]
    return delivery, sorted_pizzas


def remaining_pizzas(pizzas):
    return len([item for sublist in pizzas.values() for item in sublist])


def solve(t2, t3, t4, pizzas):
    deliveries = []

    pizza_ids = list(pizzas.keys())

    unique_pizzas = find_unique_pizzas(pizzas)

    # Sort pizzas by rareness, only works in Python 3.7+
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_pizzas = {k: v for k, v in sorted(unique_pizzas.items(), key=lambda item: len(item[1]))}
    # print("Sorted pizzas: ", sorted_pizzas)

    for _ in range(t4):
        if remaining_pizzas(sorted_pizzas) < 4:
            break
        current_delivery, sorted_pizzas = deliver_to_team(sorted_pizzas, 4)
        deliveries.append(current_delivery)

    for _ in range(t3):
        if remaining_pizzas(sorted_pizzas) < 3:
            break
        current_delivery, sorted_pizzas = deliver_to_team(sorted_pizzas, 3)
        deliveries.append(current_delivery)

    # Iterate over teams
    for _ in range(t2):
        if remaining_pizzas(sorted_pizzas) < 2:
            break
        current_delivery, sorted_pizzas = deliver_to_team(sorted_pizzas, 2)
        deliveries.append(current_delivery)

    # print("Deliveries: ", deliveries)
    return deliveries


def main():
    for file in args.file:
        t2, t3, t4, pizzas = read_file(f"input/{file}.in")
        deliveries = solve(t2, t3, t4, pizzas)
        output_file(f"output/{file}.out", deliveries)


if __name__ == "__main__":
    main()
