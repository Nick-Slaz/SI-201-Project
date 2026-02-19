# Name: Annika Gurnani
# Student ID: 29363715
# Email: agurnani@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Nick
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT hints for debugging and suggesting the general structure of the code
# Did your use of GenAI on this assignment align with your goals and guidelines in
# your Gen 
import csv

def read_input():
    penguins = []
    with open("penguins.csv", newline="") as inFile:
        reader = csv.DictReader(inFile)

        for row in reader:
            row["bill_length_mm"] = float(row["bill_length_mm"])
            row["bill_depth_mm"] = float(row["bill_depth_mm"])
            row["flipper_length_mm"] = int(row["flipper_length_mm"])
            row["body_mass_g"] = int(row["body_mass_g"])

            penguins.append(row)

    return penguins

def calc_island_flipper_lengths(penguins):
    island_flipper_lengths = {}

    for penguin in penguins:
        island = penguin["island"]
        sex = penguin["sex"]
        flipper_length = penguin["flipper_length_mm"]

        if flipper_length == "" or sex == "":
            continue

        if flipper_length > 210:
            if island not in island_flipper_lengths:
                island_flipper_lengths[island] = {"Male": 0, "Female": 0}

            if sex in island_flipper_lengths[island]:
                island_flipper_lengths[island][sex] += 1

    return island_flipper_lengths
        



def _species_avg_body_mass(penguins):
    data = {}
    averages = {}

    for penguin in penguins:
        species = penguin["species"]
        sex = penguin["sex"]
        body_mass = penguin["body_mass_g"]

        if species == "" or sex == "" or body_mass == "":
            continue

        if species not in data:
            data[species] = {
                "Male": {"total": 0, "count": 0},
                "Female": {"total": 0, "count": 0}
            }
        
        data[species][sex]["total"] += body_mass
        data[species][sex]["count"] += 1
    
    for species in data.items():
        averages[species] = {}
        
        for sex in data[species]:
            total = data[species][sex]["total"]
            count = data[species][sex]["count"]

            if count > 0:
                averages[species][sex] = total/count
            else:
                averages[species][sex] = 0
                
    return averages
            





def calculator_3(): 
    pass

def calculator_4():
    pass

def write_output():
    pass

def main():
    #calc_island_flipper_lengths()
    pass