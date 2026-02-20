# Name: Annika Gurnani
# Student ID: 29363715
# Email: agurnani@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Nick
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT hints for debugging and suggesting the general structure of the code
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? yes

import csv
import os
import sys
import unittest
import tempfile


# ------------------------
# helpers
# ------------------------
def _is_missing(x):
    return x is None or str(x).strip() == "" or str(x).strip().lower() in {"na", "nan", "none", "null"}


def _to_float(x):
    if _is_missing(x):
        return None
    try:
        return float(x)
    except ValueError:
        return None


def _to_int(x):
    if _is_missing(x):
        return None
    try:
        return int(float(x))  # handles "210.0" too
    except ValueError:
        return None


def _normalize_sex(x):
    if _is_missing(x):
        return ""
    x = str(x).strip().lower()
    if x in {"male", "female"}:
        return x
    return ""


# ------------------------
# required functions
# ------------------------
def read_input(filename="penguins.csv"):
    """
    reads penguins csv and returns a list of dict rows.
    converts numeric columns to int/float, missing -> None.
    normalizes sex to 'male'/'female' or '' if missing/unknown.
    """

    # if they pass "penguins.csv", treat it as in the same folder as this .py file
    if not os.path.isabs(filename):
        base = os.path.dirname(__file__)
        filename = os.path.join(base, filename)

    penguins = []
    with open(filename, newline="") as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            row["bill_length_mm"] = _to_float(row.get("bill_length_mm"))
            row["bill_depth_mm"] = _to_float(row.get("bill_depth_mm"))
            row["flipper_length_mm"] = _to_int(row.get("flipper_length_mm"))
            row["body_mass_g"] = _to_int(row.get("body_mass_g"))

            row["sex"] = _normalize_sex(row.get("sex"))
            row["species"] = (row.get("species") or "").strip()
            row["island"] = (row.get("island") or "").strip()

            penguins.append(row)

    return penguins


def calc_island_flipper_lengths(penguins):
    """
    counts penguins with flipper_length_mm > 210 by island and sex.
    returns: { island: {"male": count, "female": count}, ... }
    """
    out = {}
    for p in penguins:
        island = p.get("island", "")
        sex = p.get("sex", "")
        fl = p.get("flipper_length_mm")

        if island == "" or sex == "" or fl is None:
            continue
        if fl <= 210:
            continue

        if island not in out:
            out[island] = {"male": 0, "female": 0}
        out[island][sex] += 1

    return out


def species_avg_body_mass_by_sex(penguins):
    """
    average body_mass_g by species and sex (male/female).
    returns: {species: {"male": avg, "female": avg}, ...} rounded to 2 decimals.
    """
    totals = {}

    for p in penguins:
        sp = p.get("species", "")
        sex = p.get("sex", "")
        mass = p.get("body_mass_g")

        if sp == "" or sex == "" or mass is None:
            continue

        if sp not in totals:
            totals[sp] = {
                "male": {"sum": 0, "count": 0},
                "female": {"sum": 0, "count": 0}
            }

        totals[sp][sex]["sum"] += mass
        totals[sp][sex]["count"] += 1

    avgs = {}
    for sp in totals:
        avgs[sp] = {}
        for sex in ("male", "female"):
            c = totals[sp][sex]["count"]
            s = totals[sp][sex]["sum"]
            avgs[sp][sex] = round(s / c, 2) if c > 0 else 0

    return avgs


def avg_body_mass_above_flipper_avg(penguins):
    """
    compute overall avg flipper length (non-missing),
    then for each species compute avg body mass among rows
    where flipper_length_mm > overall_avg and body_mass_g exists.
    returns: {species: avg_mass} rounded to 2 decimals.
    """
    flippers = [p.get("flipper_length_mm") for p in penguins if p.get("flipper_length_mm") is not None]
    if not flippers:
        return {}

    overall_avg = sum(flippers) / len(flippers)

    totals = {}
    counts = {}

    for p in penguins:
        fl = p.get("flipper_length_mm")
        mass = p.get("body_mass_g")
        sp = p.get("species", "")

        if sp == "" or fl is None or mass is None:
            continue
        if fl <= overall_avg:
            continue

        totals[sp] = totals.get(sp, 0) + mass
        counts[sp] = counts.get(sp, 0) + 1

    return {sp: round(totals[sp] / counts[sp], 2) for sp in totals}


def gender_percentage_by_island(penguins):
    """
    for each island, percent male/female among rows that have:
      - bill_length_mm present
      - sex present (male/female)
    returns: {island: {"male": pct, "female": pct}} rounded to 2 decimals
    """
    total = {}
    male = {}

    for p in penguins:
        island = p.get("island", "")
        sex = p.get("sex", "")
        bill = p.get("bill_length_mm")

        if island == "" or sex == "" or bill is None:
            continue

        total[island] = total.get(island, 0) + 1
        male[island] = male.get(island, 0) + (1 if sex == "male" else 0)

    out = {}
    for isl in total:
        t = total[isl]
        m = male.get(isl, 0)
        f = t - m
        out[isl] = {
            "male": round((m / t) * 100, 2),
            "female": round((f / t) * 100, 2)
        }

    return out


def write_output(filename, island_flippers, species_body_mass_by_sex, avg_mass_above_flipper, gender_pct):
    """
    writes results to a text file
    """
    with open(filename, "w") as f:
        f.write("penguins results\n")
        f.write("================\n\n")

        f.write("1) count of penguins with flipper length > 210 (by island + sex)\n")
        if island_flippers:
            for island, counts in island_flippers.items():
                f.write(f"  - {island}: male={counts['male']}, female={counts['female']}\n")
        else:
            f.write("  (no results)\n")
        f.write("\n")

        f.write("2) average body mass (g) by species + sex\n")
        if species_body_mass_by_sex:
            for species, sexes in species_body_mass_by_sex.items():
                f.write(f"  - {species}: male={sexes['male']}, female={sexes['female']}\n")
        else:
            f.write("  (no results)\n")
        f.write("\n")

        f.write("3) avg body mass (g) for penguins above the overall avg flipper length (by species)\n")
        if avg_mass_above_flipper:
            for species, avg in avg_mass_above_flipper.items():
                f.write(f"  - {species}: {avg}\n")
        else:
            f.write("  (no results)\n")
        f.write("\n")

        f.write("4) gender percentage by island (filtered to rows with bill_length_mm present)\n")
        if gender_pct:
            for island, pct in gender_pct.items():
                f.write(f"  - {island}: male={pct['male']}%, female={pct['female']}%\n")
        else:
            f.write("  (no results)\n")


def main():
    penguins = read_input("penguins.csv")

    island_flippers = calc_island_flipper_lengths(penguins)
    species_body_mass = species_avg_body_mass_by_sex(penguins)
    avg_mass_above_flipper = avg_body_mass_above_flipper_avg(penguins)
    gender_pct = gender_percentage_by_island(penguins)

    print(island_flippers)
    print(species_body_mass)
    print(avg_mass_above_flipper)
    print(gender_pct)

    write_output(
        "penguins_output.txt",
        island_flippers,
        species_body_mass,
        avg_mass_above_flipper,
        gender_pct
    )


#tests
class TestPenguins(unittest.TestCase):

    def test_read_input_converts_and_normalizes(self):
        csv_text = (
            "species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex\n"
            "Adelie,Torgersen,39.1,18.7,181,3750,Male\n"
            "Adelie,Torgersen,NA,17.4,NA,3800,FEMALE\n"
        )
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "penguins.csv")
            with open(path, "w") as f:
                f.write(csv_text)

            data = read_input(path)
            self.assertEqual(data[0]["bill_length_mm"], 39.1)
            self.assertEqual(data[0]["flipper_length_mm"], 181)
            self.assertEqual(data[0]["sex"], "male")

            self.assertIsNone(data[1]["bill_length_mm"])
            self.assertIsNone(data[1]["flipper_length_mm"])
            self.assertEqual(data[1]["sex"], "female")

    def test_read_input_handles_blank_missing(self):
        csv_text = (
            "species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex\n"
            "Chinstrap,Dream,,18.0,200,,\n"
        )
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "penguins.csv")
            with open(path, "w") as f:
                f.write(csv_text)

            data = read_input(path)
            self.assertIsNone(data[0]["bill_length_mm"])
            self.assertIsNone(data[0]["body_mass_g"])
            self.assertEqual(data[0]["sex"], "")

    # calc_island_flipper_lengths 
    def test_calc_island_flipper_lengths_basic(self):
        penguins = [
            {"island": "Dream", "sex": "male", "flipper_length_mm": 215},
            {"island": "Dream", "sex": "female", "flipper_length_mm": 220},
            {"island": "Dream", "sex": "male", "flipper_length_mm": 210},
        ]
        out = calc_island_flipper_lengths(penguins)
        self.assertEqual(out["Dream"]["male"], 1)
        self.assertEqual(out["Dream"]["female"], 1)

    def test_calc_island_flipper_lengths_skips_missing(self):
        penguins = [
            {"island": "Biscoe", "sex": "", "flipper_length_mm": 230},
            {"island": "Biscoe", "sex": "male", "flipper_length_mm": None},
            {"island": "", "sex": "male", "flipper_length_mm": 240},
        ]
        out = calc_island_flipper_lengths(penguins)
        self.assertEqual(out, {})

    # species_avg_body_mass_by_sex 
    def test_species_avg_body_mass_by_sex_basic(self):
        penguins = [
            {"species": "Adelie", "sex": "male", "body_mass_g": 4000},
            {"species": "Adelie", "sex": "male", "body_mass_g": 4200},
            {"species": "Adelie", "sex": "female", "body_mass_g": 3500},
        ]
        out = species_avg_body_mass_by_sex(penguins)
        self.assertEqual(out["Adelie"]["male"], 4100.00)
        self.assertEqual(out["Adelie"]["female"], 3500.00)

    def test_species_avg_body_mass_by_sex_ignores_missing(self):
        penguins = [
            {"species": "Gentoo", "sex": "male", "body_mass_g": None},
            {"species": "Gentoo", "sex": "", "body_mass_g": 5000},
        ]
        out = species_avg_body_mass_by_sex(penguins)
        self.assertEqual(out, {})

    # avg_body_mass_above_flipper_avg 
    def test_avg_body_mass_above_flipper_avg_basic(self):
        penguins = [
            {"species": "Adelie", "flipper_length_mm": 200, "body_mass_g": 4000},
            {"species": "Adelie", "flipper_length_mm": 220, "body_mass_g": 4100},
            {"species": "Gentoo", "flipper_length_mm": 240, "body_mass_g": 5000},
        ]
        out = avg_body_mass_above_flipper_avg(penguins)
        self.assertEqual(out, {"Gentoo": 5000.00})

    def test_avg_body_mass_above_flipper_avg_handles_missing(self):
        penguins = [
            {"species": "Adelie", "flipper_length_mm": None, "body_mass_g": 4000},
            {"species": "Adelie", "flipper_length_mm": 230, "body_mass_g": None},
        ]
        out = avg_body_mass_above_flipper_avg(penguins)
        self.assertEqual(out, {})

    # gender_percentage_by_island
    def test_gender_percentage_by_island_basic(self):
        penguins = [
            {"island": "Dream", "sex": "male", "bill_length_mm": 40.0},
            {"island": "Dream", "sex": "female", "bill_length_mm": 38.0},
            {"island": "Dream", "sex": "male", "bill_length_mm": 41.0},
        ]
        out = gender_percentage_by_island(penguins)
        self.assertEqual(out["Dream"]["male"], 66.67)
        self.assertEqual(out["Dream"]["female"], 33.33)

    def test_gender_percentage_by_island_skips_missing_bill_or_sex(self):
        penguins = [
            {"island": "Biscoe", "sex": "male", "bill_length_mm": None},
            {"island": "Biscoe", "sex": "", "bill_length_mm": 45.0},
        ]
        out = gender_percentage_by_island(penguins)
        self.assertEqual(out, {})

    # write_output 
    def test_write_output_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            outpath = os.path.join(d, "out.txt")
            write_output(
                outpath,
                {"Dream": {"male": 1, "female": 2}},
                {"Adelie": {"male": 4100.0, "female": 3500.0}},
                {"Gentoo": 5000.0},
                {"Dream": {"male": 60.0, "female": 40.0}},
            )
            self.assertTrue(os.path.exists(outpath))
            with open(outpath) as f:
                text = f.read()
            self.assertIn("penguins results", text)
            self.assertIn("Dream: male=1, female=2", text)

    def test_write_output_handles_empty_results(self):
        with tempfile.TemporaryDirectory() as d:
            outpath = os.path.join(d, "out.txt")
            write_output(outpath, {}, {}, {}, {})
            with open(outpath) as f:
                text = f.read()
            self.assertIn("(no results)", text)


if __name__ == "__main__":
    # run tests:  python3 penguins_analysis.py test
    # run program: python3 penguins_analysis.py
    if "test" in sys.argv:
        unittest.main(argv=["first-arg-is-ignored"])
    else:
        main()
