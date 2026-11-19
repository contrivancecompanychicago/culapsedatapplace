import json

# Load the JSON code
with open("game_code.json") as f:
    game_code = json.load(f)

# Get the ant's strategy
ant_strategy = game_code["ant"]["strategies"][0]

# Get the mosquito's strategy
mosquito_strategy = game_code["mosquito"]["strategies"][0]

# Calculate the probability of the ant using a stalking strategy
probability = game_code["ant"]["payoffs"][ant_strategy][mosquito_strategy]

print(probability)
