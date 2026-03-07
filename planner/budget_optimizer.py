def apply_budget(places, budget):
    selected = []
    total = 0

    for p in places:
        if total + p['cost'] <= budget:
            selected.append(p)
            total += p['cost']

    return selected