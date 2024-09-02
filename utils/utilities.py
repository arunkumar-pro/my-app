import random


def generate_random_data(num_entries=5):
    names = [
        "Oliver", "Charlotte", "Noah", "Amelia", "Liam", "Sophia", "Elijah", "Isabella", "James", "Mia",
        "Benjamin", "Evelyn", "Lucas", "Harper", "Mason", "Ava", "Ethan", "Luna", "Alexander", "Chloe",
        "Henry", "Aria", "Sebastian", "Ella", "Jackson", "Ellie", "Aiden", "Scarlett", "Matthew", "Emily",
        "Samuel", "Layla", "David", "Sofia", "Joseph", "Mila", "Carter", "Avery", "Owen", "Camila",
        "Wyatt", "Gianna", "John", "Abigail", "Jack", "Lily", "Luke", "Grace", "Jayden", "Victoria",
        "Dylan", "Riley", "Levi", "Zoe", "Isaac", "Nora", "Gabriel", "Hazel", "Julian", "Aurora",
        "Mateo", "Savannah", "Anthony", "Penelope", "Jaxon", "Lillian", "Grayson", "Addison", "Leo", "Aubrey",
        "Josiah", "Stella", "Christopher", "Elena", "Andrew", "Natalie", "Thomas", "Hannah", "Charles", "Brooklyn",
        "Caleb", "Leah", "Isaiah", "Zoey", "Ryan", "Paisley", "Nathan", "Claire", "Adrian", "Skylar",
        "Christian", "Lucy", "Hunter", "Everly", "Eli", "Anna", "Jonathan", "Caroline", "Connor", "Madelyn"
    ]

    countries = [
        "United States", "Canada", "Mexico", "Brazil", "Argentina",
        "United Kingdom", "Germany", "France", "Italy", "Spain",
        "Australia", "New Zealand", "China", "Japan", "South Korea",
        "India", "Pakistan", "Bangladesh", "Russia", "Ukraine",
        "South Africa", "Egypt", "Nigeria", "Kenya", "Morocco",
        "Turkey", "Saudi Arabia", "United Arab Emirates", "Israel", "Iran",
        "Indonesia", "Malaysia", "Thailand", "Vietnam", "Philippines",
        "Singapore", "Sri Lanka", "Nepal", "Bhutan", "Maldives",
        "Greece", "Portugal", "Netherlands", "Sweden", "Norway",
        "Denmark", "Finland", "Switzerland", "Austria", "Belgium"
    ]

    data = []

    for _ in range(num_entries):
        entry = {
            "name": random.choice(names),
            "age": random.randint(18, 70),
            "phone": str(random.randint(1000000, 9999999)),
            "country": random.choice(countries)
        }
        data.append(entry)

    return data


def modify_id_filed(data):
    for rec in data:
        rec["_id"] = str(rec.get("_id"))
    return data