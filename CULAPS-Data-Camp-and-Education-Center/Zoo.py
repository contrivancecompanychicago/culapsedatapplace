import json

def main():
  # Load the JSON file
  with open("zoo.json", "r") as f:
    data = json.load(f)

  # Initialize the animals
  ant = Animal(data["ant"])
  mosquito = Animal(data["mosquito"])
  turtle = Animal(data["turtle"])

  # Play the game
  while True:
    # Get the animals' strategies
    ant_strategy = ant.get_strategy()
    mosquito_strategy = mosquito.get_strategy()
    turtle_strategy = turtle.get_strategy()

    # Calculate the payoffs
    ant_payoff = ant.calculate_payoff(mosquito_strategy, turtle_strategy)
    mosquito_payoff = mosquito.calculate_payoff(ant_strategy, turtle_strategy)
    turtle_payoff = turtle.calculate_payoff(ant_strategy, mosquito_strategy)

    # Print the payoffs
    print("Ant:", ant_payoff)
    print("Mosquito:", mosquito_payoff)
    print("Turtle:", turtle_payoff)

    # Check if the game is over
    if ant_payoff == "ant gets food" or mosquito_payoff == "mosquito gets food" or turtle_payoff == "turtle is bitten":
      break

if __name__ == "__main__":
  main()
