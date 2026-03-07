def schedule(places, days):
    schedule = {}
    per_day = max(1, len(places)//days)

    idx = 0
    for d in range(1, days+1):
        schedule[f"Day {d}"] = places[idx:idx+per_day]
        idx += per_day

    return schedule