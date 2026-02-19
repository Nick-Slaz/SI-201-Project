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
            





def avg_body_mass_above_flipper_avg(data):

    flippers = []
    for row in data:
        if row["flipper_length_mm"] != "":
            flippers.append(float(row["flipper_length_mm"]))

    if not flippers:
        return {}

    overall_avg = sum(flippers) / len(flippers)

    species_totals = {}
    species_counts = {}

    for row in data:
        if row["flipper_length_mm"] == "" or row["body_mass_g"] == "":
            continue

        fl = float(row["flipper_length_mm"])
        body_mass = float(row["body_mass_g"])
        species = row["species"]

        if fl > overall_avg:
            if species not in species_totals:
                species_totals[species] = 0
                species_counts[species] = 0

            species_totals[species] += body_mass
            species_counts[species] += 1

    results = {}
    for sp in species_totals:
        results[sp] = species_totals[sp] / species_counts[sp]

    return results

def gender_percentage_by_island(data):

    island_counts = {}
    island_male = {}

    for row in data:
        island = row["island"]
        sex = row["sex"]
        bill = row["bill_length_mm"]

        if sex == "" or bill == "":
            continue

        if island not in island_counts:
            island_counts[island] = 0
            island_male[island] = 0

        island_counts[island] += 1
        if sex.lower() == "male":
            island_male[island] += 1

    results = {}
    for isl in island_counts:
        male_count = island_male[isl]
        total = island_counts[isl]
        female_count = total - male_count

        male_pct = (male_count / total) * 100
        female_pct = (female_count / total) * 100

        results[isl] = {
            "male": round(male_pct, 2),
            "female": round(female_pct, 2)
        }

    return results

def write_output():
    pass

def main():
    pass