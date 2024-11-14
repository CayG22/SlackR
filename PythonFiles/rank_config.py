#Ranks
RANKS = {
    "Titanium": 0.9,
    "Zinc": .75,
    "Lead": .6,
    "Palladium": .4,
    "Nickel": .0
}

#Archetypes
ARCHETYPES = {
    "Clutch King": lambda stats: stats.get('Clutches', 0) > 50,
    "Engager": lambda stats: stats.get('first_kills', 0) > 150,
    "Sniper": lambda stats: stats.get('hs_perc', 0) > 27,
    "Rusher": lambda stats: stats.get('first_deaths', 0) > 150,
    "Assasin": lambda stats: stats.get('knife_kills', 0) > 5,
    "Straight Up Winner": lambda stats: stats.get('winp',0) > 53,
}