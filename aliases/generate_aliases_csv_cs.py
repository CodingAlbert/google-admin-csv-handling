import nltk
import random
import csv
import sys
import os
import pickle
from nltk.corpus import wordnet as wn
from deep_translator import GoogleTranslator
from unidecode import unidecode

ADJECTIVES_FILE = 'adjectives.pkl'
ANIMALS_FILE = 'animals.pkl'

# Expanded list of offensive words to exclude
OFFENSIVE_WORDS = set([
    "racist", "fascist", "nigger", "aborted", "hideous", "stupid", "idiot", "moron", "dumb", "ugly",
    "bitch", "bastard", "damn", "damned", "hell", "asshole", "shit", "fuck", "fucker", "fucking",
    "cunt", "dick", "prick", "pussy", "slut", "whore", "retard", "retarded", "crap", "crappy", 
    "faggot", "gay", "lesbian", "homosexual", "queer", "tranny", "transgender", "fat", "obese",
    "skinny", "anorexic", "junkie", "addict", "alcoholic", "drunk", "druggie", "terrorist", 
    "murderer", "killer", "thief", "crook", "criminal", "thug", "pervert", "pedophile",
    "nazi", "negro", "spic", "chink", "gook", "wop", "kike", "dyke", "cracker", "redneck",
    "hillbilly", "hobo", "beggar", "bum", "tramp", "hobo", "beggar", "disease", "infection",
    "virus", "bacteria", "plague", "parasite", "maggot", "cockroach", "rat", "snake", "vile",
    "disgusting", "filthy", "nasty", "gross", "obscene", "vulgar", "heinous", "abominable",
    "deplorable", "dreadful", "evil", "wicked", "malevolent", "malicious", "sinister", "villainous",
    "abhorrent", "despicable", "loathsome", "repugnant", "repulsive", "revolting", "offensive",
    "drugged","stoned","cursed","sexual","vulvar","rectal","hindi","arab","christian","goddamn",
    "muslim","slutty","breastless","whory","dicky","threesome","orgy","phallic","penile","horny",
    "zionist","jewish"
])

def count_syllables(word):
    """ Count the number of syllables in a word using a simple heuristic """
    vowels = 'aeiouyáéíóúůýěščřž'
    word = word.lower().strip(".:;?!")
    if len(word) == 0:
        return 0
    syllable_count = 0
    if word[0] in vowels:
        syllable_count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            syllable_count += 1
    if word.endswith("e"):
        syllable_count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count = 1
    return syllable_count

# Function to get strictly two-syllable animal names using hypernyms
def fetch_animal_names():
    print("Fetching animal names...")
    animals = set()
    visited = set()  # To prevent redundancy
    animal_synset = wn.synset('animal.n.01')
    queue = [animal_synset]
    while queue:
        syn = queue.pop(0)
        if syn not in visited:
            visited.add(syn)
            for lemma in syn.lemmas():
                name = lemma.name().replace('_', ' ')
                if count_syllables(name) == 2:
                    animals.add(name.lower())
            queue.extend(syn.hyponyms())
    print(f"Fetched {len(animals)} animal names.")
    return list(animals)

# Function to get two-syllable adjectives from WordNet
def fetch_adjectives():
    print("Fetching adjectives...")
    adjectives = set()
    for synset in wn.all_synsets(wn.ADJ):
        for lemma in synset.lemmas():
            name = lemma.name().replace('_', ' ')
            if (
                count_syllables(name) == 2 and
                not any(char.isdigit() or char == '.' for char in name) and
                name not in OFFENSIVE_WORDS
            ):
                adjectives.add(name.lower())
    print(f"Fetched {len(adjectives)} adjectives.")
    return list(adjectives)

def load_or_fetch_data():
    if os.path.exists(ADJECTIVES_FILE) and os.path.exists(ANIMALS_FILE):
        with open(ADJECTIVES_FILE, 'rb') as f:
            adjectives = pickle.load(f)
        with open(ANIMALS_FILE, 'rb') as f:
            animals = pickle.load(f)
        print(f"Loaded {len(adjectives)} adjectives and {len(animals)} animals from files.")
    else:
        # Ensure required NLTK resources are downloaded only if files are not present
        print("Downloading NLTK data...")
        nltk.download('wordnet')
        nltk.download('omw-1.4')

        adjectives = fetch_adjectives()
        animals = fetch_animal_names()
        with open(ADJECTIVES_FILE, 'wb') as f:
            pickle.dump(adjectives, f)
        with open(ANIMALS_FILE, 'wb') as f:
            pickle.dump(animals, f)
        print(f"Saved {len(adjectives)} adjectives and {len(animals)} animals to files.")
    return adjectives, animals

# Translate word pairs
def translate_pair(adjective, animal):
    translator = GoogleTranslator(source='auto', target='cs')
    try:
        combined = f"{adjective} {animal}"
        translated_combined = translator.translate(combined)
        parts = translated_combined.split()
        
        if len(parts) < 2:
            raise ValueError(f"Unexpected translation result: {translated_combined}")
        
        translated_adjective_parts = parts[:-1]
        translated_animal_part = parts[-1]
        
        translated_adjective = "".join(translated_adjective_parts).replace("-", "").replace(" ", "").replace("'", "")
        translated_animal = translated_animal_part.replace("-", "").replace(" ", "").replace("'", "")
        
        full_translation = f"{translated_adjective} {translated_animal}"
        if count_syllables(full_translation) > 6:
            return None
        
        translated_adjective = unidecode(translated_adjective)
        translated_animal = unidecode(translated_animal)

        return f"{translated_adjective}.{translated_animal}"
    except Exception as e:
        print(f"Error translating pair ({adjective}, {animal}): {e}")
        return None

# Generate aliases with fullstop instead of underscore
def generate_aliases(animals, adjectives, num_aliases):
    unique_aliases = set()
    while len(unique_aliases) < num_aliases:
        animal = random.choice(animals)
        adjective = random.choice(adjectives)
        alias = translate_pair(adjective, animal)
        if alias:
            unique_aliases.add(alias)
        else:
            print(f"Rejected alias ({adjective}, {animal}) due to syllable limit or error.")
    return list(unique_aliases)

# Main script operation
def main(num_aliases):
    adjectives, animals = load_or_fetch_data()

    max_combinations = len(animals) * len(adjectives)
    if num_aliases > max_combinations:
        print(f"Warning: The number of aliases requested ({num_aliases}) exceeds the maximum number of unique combinations ({max_combinations}).")
        num_aliases = max_combinations

    aliases = generate_aliases(animals, adjectives, num_aliases)

    # Save aliases to a CSV file
    with open('animal_aliases_cs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for alias in aliases:
            writer.writerow([alias])

    print(f"Generated {num_aliases} aliases and saved them to 'animal_aliases_cs.csv'")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <number_of_aliases>")
    else:
        try:
            num_aliases = int(sys.argv[1])
            main(num_aliases)
        except ValueError:
            print("The number of aliases must be an integer.")
