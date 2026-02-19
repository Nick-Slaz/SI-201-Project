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

def main():
    pass

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

def calculation_1():
    pass

def calculation_2():
    pass

def calculation_3(): 
    pass

def calcultion_4():
    pass

def write_output():
    pass

