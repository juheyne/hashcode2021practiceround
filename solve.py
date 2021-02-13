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

        print(pizzas)
        return int(t2), int(t3), int(t4), pizzas


def output_file(file, deliveries):
    print(deliveries)
    with open(file, "w+") as f:
        f.write(f"{str(len(deliveries))}\n")
        print(str(len(deliveries)))
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
    :return: most_matching_set: union of best matching set and passed set_of_ingredients
    """
    most_matching_count = -1
    most_matching_id = -1
    most_matching_set = {}
    for key, value in dict_ingredient_tuple_to_ids.items():
        new_set = set_of_ingredient.union(set(key))
        if len(new_set) > most_matching_count:
            most_matching_count = len(new_set)
            most_matching_set = new_set
            most_matching_id = value[0]
    return most_matching_id, most_matching_set


def solve(t2, t3, t4, pizzas):
    deliveries = []

    pizza_ids = list(pizzas.keys())

    unique_pizzas = find_unique_pizzas(pizzas)
    print("Unique pizzas: ", unique_pizzas)

    # Sort pizzas by rareness, only works in Python 3.7+
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    pizzas_sorted = {k: v for k, v in sorted(unique_pizzas.items(), key=lambda item: len(item[1]))}

    for toppings, pizza_ids in pizzas_sorted.items():
        print(toppings, ":", pizza_ids)

    # Iterate over teams
    for _ in range(t2):
        if len(pizza_ids) < 2:
            break
        current_delivery = []
        for i in range(2):
            current_delivery.append(pizza_ids.pop())
        deliveries.append(current_delivery)

    for _ in range(t3):
        if len(pizza_ids) < 3:
            break
        current_delivery = []
        for i in range(3):
            current_delivery.append(pizza_ids.pop())
        deliveries.append(current_delivery)

    for _ in range(t4):
        if len(pizza_ids) < 4:
            break
        current_delivery = []
        for i in range(4):
            current_delivery.append(pizza_ids.pop())
        deliveries.append(current_delivery)

    return deliveries


def main():
    for file in args.file:
        t2, t3, t4, pizzas = read_file(f"input/{file}.in")
        deliveries = solve(t2, t3, t4, pizzas)
        output_file(f"output/{file}.out", deliveries)


if __name__ == "__main__":
    main()
