# core_logic/processor.py

import os, re, io
from contextlib import redirect_stdout
from collections import Counter

spacing_symbol = "#"
center_val = 80

class Number:
    def __init__(self, value):
        self.value = value
        self.title = self.set_title()
        self.energy = self.set_energy()
        self.characteristics = self.set_characteristics()
        self.relationships = self.set_relationships()
        #self.number_group = self.set_number_group()
        self.health_intro = self.set_health_intros()
        self.affirmations = self.set_affirmations()
        self.attributes = self.set_attributes()

    def get_value(self):
        return self.value

    def set_title(self):
        titles = {
            1: "The Warrior",
            2: "The Mediator",
            3: "The Child",
            4: "The Worker",
            5: "The Traveler",
            6: "The Caretaker",
            7: "The Loner",
            8: "The Executive",
            9: "The Secret Master",
            11: "The Old Soul",
            22: "The Master Builder",
            33: "The Master Teacher"
        }
        return titles.get(self.value, "Unknown Title")

    def set_energy(self):
        energies = {
            1: "Masculine Energy",
            2: "Feminine Energy",
            3: "Creative Energy",
            4: "Controlling Energy",
            5: "Freedom Energy",
            6: "Nurturing Energy",
            7: "Intellectual Energy",
            8: "Commanding Energy",
            9: "Completion Energy",
            11: "Intuitive Energy",
            22: "Manifestation Energy",
            33: "Compassion Energy"
        }
        return energies.get(self.value, "Unknown Energy")

    def set_characteristics(self):
        characteristics = {
            1: ["Aggressive & Competitive", "Independant and Self-Motivated"],
            2: ["Soft & Passive", "Diplomatic and Peaceful"],
            3: ["Effective Communicator", "Simple Pleasures"],
            4: ["Seeks Law & Order [Security]", "Responsible and Disciplined"],
            5: ["Embraces Change & Risk", "Entertainment and Hospitality"],
            6: ["Friendly & Loving", "Balanced and Responsible"],
            7: ["Introverted & Intuitive", "Unlucky Truth Seeker"],
            8: ["Needs Spiritual & Material Freedom", "Karmically Sensitive"],
            9: ["Leadership and Humanitarian Instincts", "Quick and Effective Thinker"],
            11: ["Charisma & Idealism", "MASTER NUMBER"],
            22: ["Peace & Calm", "MASTER NUMBER"],
            33: ["Selfless Giver & Cosmic Guardian", "MASTER NUMBER"]
        }
        return characteristics.get(self.value, ["Unknown Characteristics"])
    
    def set_relationships(self):
        relationships = {
            1: ([1, 5, 7], [2, 3, 9], [4, 6, 8], []),
            2: ([2, 4, 8], [1, 3, 6, 9], [5, 7], []),
            3: ([3, 6, 9], [1, 2, 5], [4, 7, 8], []),
            4: ([2, 4, 8], [6, 7], [1, 3, 5, 9], []),
            5: ([1, 5, 7], [3, 9], [2, 4, 6], [8]),
            6: ([3, 6, 9], [2, 4, 8], [1, 5, 7], []),
            7: ([1, 5, 7], [4], [2, 3, 6, 8, 9], []),
            8: ([2, 4, 8], [5, 6], [1, 3, 7, 9], []),
            9: ([3, 6, 9], [1, 2, 5], [4, 7, 8], []),
            11: ([2, 4, 8], [1, 3, 6, 9], [5, 7], []),
            22: ([2, 4, 8], [6, 7], [1, 3, 5, 9], []),
            33: ([3, 6, 9], [2, 4, 8], [1, 5, 7], [])
        }
        return relationships.get(self.value, ([],[],[],[]))

    #def set_number_group(self):

    def set_health_intros(self):
        health_intros = {
            1: "A healthy 1 is independent, self-motivated, a hard worker.",
            2: "A healthy 2 is harmonious, loving, and a peacemaker.",
            3: "A healthy 3 is upbeat, enthusiastic, and optimistic about themselves and others.",
            4: "A healthy 4 would be seeking knowledge, providing security, and sharing expertise through teaching.",
            5: "A healthy 5 celebrates life, and is adventurous and passionate.",
            6: "The healthy 6 seeks harmony, is nurturing and wise.",
            7: "A healthy 7 is intelligent. They have a gentle spirit and intuition.",
            8: "A healthy 8 is ambitious, has a head for business, and real executive ability.",
            9: "A healthy 9 has compassion for others and is a dynamic leader.",
            11: "A healthy 2 is harmonious, loving, and a peacemaker.",
            22: "A healthy 4 would be seeking knowledge, providing security, and sharing expertise through teaching.",
            33: "The healthy 6 seeks harmony, is nurturing and wise."
        }
        return health_intros.get(self.value, "Unknown Health Introduction")

    def set_affirmations(self):
        affirmations = {
            1: ["To Combat Self-Criticism: \"I recognize the miracle of my being. I am enough.\"",
                "To Accept Yourself: \"I am perfectly content to be me. I am good enough just as I am.\"",
                "Heart Attacks: \"My heart beats with the rhythm of life itself. It is growing stronger every day.\""],
            2: ["When Overwhelmed: \"I am the calm expression of peace and see the love in everybody.\"",
                "Cancers: \"I affirm the complete perfection of the universe, I am a child of the universe and I live in perfect love and joy.\"",
                "Anorexia/Bulimia: \"I love myself and I welcome life-giving nourishment for my body from the endless abundance of life.\""],
            3: ["Feeling Stuck: \"I welcome my fame and fortune today\"",
                "Negativity: \"I trust the process of life, and in the movies of my mind, I am loved and at peace.\"",
                "Throat Problems: \"What I say does matter. I am heard and I do make a difference. Live is all around me.\""],
            4: ["Overthinking: \"I do not fear the future. Today is my most precious gift, and I am safe.\"",
                "Argumentative: \"I speak with kindness and love. I look for the good in everybody.\""],
            5: ["Vice Problems: \"I'm willing to change the thoughts that created this condition\"",
                "Negativity: \"I easily ask for what I need. Life supports me completely\"",
                "Cancers: \"I affirm the complete perfection of the universe, I am a child of the universe and I live in perfect love and joy.\""],
            6: ["Finding Love: \"I welcome a loving nurturing relationship with a (man/woman) who will be emotionally available to me, who will be honest, passionate and funny, who will be my equal, and my life partner, (include your own desires)\"",
                "Pedestalizing: \"I see with eyes of love. There's a harmonious solution and I accept it now.\"",
                "Over-eating: \"I love myself and I welcome life-giving nourishment for my body from the endless abundance of life.\""],
            7: ["Escapism: \"I breathe in life freely and trust the flow and process of life.\"",
                "Breaking Down: \"Divine right action is taking place at all times.\""],
            8: ["Workaholism: \"I believe in infinite abundance and the money is always there.\"",
                "Betrayal: \"Each day I live in the moment, by forgiving those in my past.\"",
                "Heart Attacks: \"My heart beats with the rhythm of life itself. It is growing stronger every day.\""],
            9: ["Grudges: \"I joyfully release all of the past and let only love surround me.\""],
            11: ["When Overwhelmed: \"I am the calm expression of peace and see the love in everybody.\"",
                "Cancers: \"I affirm the complete perfection of the universe, I am a child of the universe and I live in perfect love and joy.\"",
                "Anorexia/Bulimia: \"I love myself and I welcome life-giving nourishment for my body from the endless abundance of life.\""],
            22: ["Overthinking: \"I do not fear the future. Today is my most precious gift, and I am safe.\"",
                "Argumentative: \"I speak with kindness and love. I look for the good in everybody.\""],
            33: ["Finding Love: \"I welcome a loving nurturing relationship with a (man/woman) who will be emotionally available to me, who will be honest, passionate and funny, who will be my equal, and my life partner, (include your own desires)\"",
                "Pedestalizing: \"I see with eyes of love. There's a harmonious solution and I accept it now.\"",
                "Over-eating: \"I love myself and I welcome life-giving nourishment for my body from the endless abundance of life.\""],
        }
        return affirmations.get(self.value, ["Unknown Affirmations"])

    def set_attributes(self):
        attributes = {
            1: ["1 • Issues of the Ego Self", 
                "Positive: Self-directed, leader, paradigm buster, innovator, assertive, energetic, balanced, follows internal guidance, an initiator, comfortable with self",
                "Negative: Passive, aggressive, egocentric, low self-esteem, fearful, timid, arrogant, a zealot, a bully, no sense of self"],
            2: ["2 • Issues Involving Others", 
                "Positive: Sensitive, intuitive, cooperative, a mediator/arbitrator, organizer, harmonizer, friendly, communicates in timely fashion, detail oriented, tactful, loyal, has a good voice",
                "Negative: Subservient, shy, overly sentimental, timid, careless about 'things', codependent, does not speak up for self, self-centered, difficulty letting go of emotional and sentimental attachments, blunt, insensitive, has difficulty working with others-not a team player, hides emotions, could be nonverbal, may beat people with the 'hammer of truth'"],
            3: ["3 • Issues Involving Communication, Social Interactions, Feelings of Inadequacy", 
                "Positive: Joyful, witty, artistic, charismatic, charming, creative, intelligent, optimistic, communicative, extroverted, visionary, musical, good sense of humor —likes to laugh",
                "Negative: Moody/emotional, unforgiving, scattered, introverted, exaggerates, vain, feelings of inferiority or inadequacy, leaves things unfinished, sarcastic, grandiose plans, jealous, concerned about being judged, temperamental, ill-tempered, a bit of a gossip"],
            4: ["4 • Issues Involving Details and 'Getting Things Done'", 
                "Positive: Organized, an architect, a builder, systematic, logical, dependable, practical, a manager, ability to totally focus on a task, a logician",
                "Negative: Prejudicial, a reactionary, a procrastinator, unimaginative, gets lost in minutiac, stubborn, goes 'by the book', confrontational, dull, hides in logic, can be hateful"],
            5: ["5 • Issues Involving Change and Movement", 
                "Positive: Flexible, freedom loving, physical, enjoys life, loves innovation and change, curious, can be moderate, balanced, easily goes with the flow",
                "Negative: Unbalanced - too rigid or too yielding, impulsive, self-indulgent, inconsistent, promiscuous, indulges to excess, deals with concepts not details, always in a hurry"],
            6: ["6 • Issues Involving Family, Community, Relationships, Responsibility", 
                "Positive: Responsible, an advisor/counselor/mentor, protector, nurturer, humanitarian, service oriented, domestic, compassionate",
                "Negative: A perfectionist, a martyr, nosy, overly protective, a giver of unsought advice, codependent, avoids obligations/commitments/relationships/responsibility, needs to be in control"],
            7: ["7 • Issues Involving Abandonment, Trust, Skepticism, and Control", 
                "Positive: Trusting, spiritual, intuitive, psychic, introspective, empathetic, objective, open, vulnerable, a seeker of knowledge, patient, insightful, analytical, can see all sides of an issue",
                "Negative: Controlling, fearful, distrustful, impatient, emotionally closed, mental or emotional paralysis from being overly analytical, socially/emotionally disconnected, a zealot, a martyr, messianic feelings, codependent—a need to be needed"],
            8: ["8 • Issues Involving Power, Money, Control, and Status", 
                "Positive: Initiates/delegates/orchestrates, logical, likes to be in charge, a natural leader, makes it happen, good at politics/business/commerce/leading institutions or organizations, 'walks the talk', looks good in any kind of attire, possesses knowledge, wisdom, and expertise",
                "Negative: Easily frustrated, temperamental, extravagant/cheap, dictatorial, stubborn, materialistic, demands recognition, mean, a bully, fearful of using personal power, can be disloyal if he or she feels slighted or ignored, has a fear of success, whatever money comes is always needed for higher than expected expenses, may tend to avoid the world of business and commerce but complain about not having enough money"],
            9: ["9 • Issues Involving Selflessness", 
                "Positive: Selfless, loves unconditionally, compassionate, embraces brotherhood, a natural actor, loves long-distance travel, comfortable with all strata of society, works to raise the level of self-awareness on the planet, has let go of ego issues and embraced the higher Self",
                "Negative: Egotistical, needs recognition/appreciation/thanks for 'good deeds', has difficulty letting go, can be fearful of showing any emotion, can be emotionally isolated or codependent, can be an 'emotional pin cushion' (i.e., holds the emotions and feelings of others like a reservoir holds water)"],
            11: ["11 • Higher Vibration of 2: Issues Involving Others",
                "Positive: Sensitive, intuitive, cooperative, a mediator/arbitrator, organizer, harmonizer, friendly, communicates in timely fashion, detail oriented, tactful, loyal, has a good voice",
                "Negative: Subservient, shy, overly sentimental, timid, careless about 'things', codependent, does not speak up for self, self-centered, difficulty letting go of emotional and sentimental attachments, blunt, insensitive, has difficulty working with others-not a team player, hides emotions, could be nonverbal, may beat people with the 'hammer of truth'"],
            22: ["22 • Higher Vibration of 4: Issues Involving Details and 'Getting Things Done'", 
                "Positive: Organized, an architect, a builder, systematic, logical, dependable, practical, a manager, ability to totally focus on a task, a logician",
                "Negative: Prejudicial, a reactionary, a procrastinator, unimaginative, gets lost in minutiac, stubborn, goes 'by the book', confrontational, dull, hides in logic, can be hateful"],
            33: ["33 • Higher Vibration of 6: Issues Involving Family, Community, Relationships, Responsibility", 
                "Positive: Responsible, an advisor/counselor/mentor, protector, nurturer, humanitarian, service oriented, domestic, compassionate",
                "Negative: A perfectionist, a martyr, nosy, overly protective, a giver of unsought advice, codependent, avoids obligations/commitments/relationships/responsibility, needs to be in control"]
        }
        return attributes.get(self.value, ["Unknown Attributes"])


    def print_numerology_characteristics(self):
        print(f" - {self.title} ({self.energy})")
        for characteristic in self.characteristics:
            print(f" - {characteristic}")

    def print_number_relationships(self):
        natural_numbers, compatible_numbers, challenge_numbers, neutral_numbers = self.relationships
        print("Life Path: (", self.value,")", self.title)
        print("Natural Match Numbers:", ", ".join(map(str, natural_numbers)))
        print("Compatible Numbers:", ", ".join(map(str, compatible_numbers)))
        print("Challenge Numbers:", ", ".join(map(str, challenge_numbers)))
        if neutral_numbers:
            print("Neutral Numbers:", ", ".join(map(str, neutral_numbers)))

    def print_health_intro(self):
        print(self.health_intro)

    def print_affirmations(self):
        for affirmation in self.affirmations:
        # Split the affirmation into chunks at spaces while ensuring each chunk is as close to 80 characters as possible
            words = affirmation.split()
            chunks = []
            current_chunk = ""
            for word in words:
                if len(current_chunk) + len(word) <= 80:
                    current_chunk += word + " "
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = word + " "
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Print each chunk on a new line
            for chunk in chunks:
                print(chunk)

    def print_attributes(self):
        for attributes in self.attributes:
            words = attributes.split()
            chunks = []
            current_chunk = ""
            for word in words:
                if len(current_chunk) + len(word) <= 80:
                    current_chunk += word + " "
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = word + " "
            if current_chunk:
                chunks.append(current_chunk.strip())
            for chunk in chunks:
                print(chunk)

    @staticmethod
    def get_number_class(value):
        numbers = {
            1: one, 2: two, 3: three, 4: four, 5: five,
            6: six, 7: seven, 8: eight, 9: nine,
            11: eleven, 22: twenty_two, 33: thirty_three
        }
        return numbers.get(value, None)

    # String representation of the object
    def __str__(self):
        return str(self.value)

zero = Number(0)
one = Number(1)
two = Number(2)
three = Number(3)
four = Number(4)
five = Number(5)
six = Number(6)
seven = Number(7)
eight = Number(8)
nine = Number(9)
eleven = Number(11)
twenty_two = Number(22)
thirty_three = Number(33)

class Person:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
        self.soul_urge = zero
        self.personality = zero
        self.destiny = zero
        self.day_of_birth = zero
        self.life_path = zero
        self.attitude = zero

        if self.name:
            self.soul_urge = self.set_soul_urge()
            self.personality = self.set_personality()
            self.destiny = self.set_destiny()
        
        if self.birthday:    
            self.day_of_birth = self.set_day_of_birth()
            self.life_path = self.set_life_path()
            self.attitude = self.set_attitude()


    def get_name(self):
        return self.name

    def get_birthday(self):
        return self.birthday

    def get_soul_urge(self):
        return self.soul_urge

    def get_personality(self):
        return self.personality

    def get_destiny(self):
        return self.destiny

    def get_day_of_birth(self):
        return self.day_of_birth

    def get_life_path(self):
        return self.life_path

    def get_attitude(self):
        return self.attitude

    def get_numbers(self):
        numbers = [self.soul_urge, self.personality, self.destiny,
                   self.day_of_birth, self.life_path, self.attitude]
        return [number.get_value() for number in numbers if number is not None]

    def set_soul_urge(self):
        vowel_total = calculate_letter_total(filter(lambda x: x in "aeiou", self.name))
        reduced_vowel_sequence = reduce_and_store_totals(vowel_total)
        return Number.get_number_class(parse_sequence(reduced_vowel_sequence))      

    def set_personality(self):
        consonant_total = calculate_letter_total(filter(lambda x: x in "bcdfghjklmnpqrstvwxyz", self.name))
        reduced_consonant_sequence = reduce_and_store_totals(consonant_total)
        return Number.get_number_class(parse_sequence(reduced_consonant_sequence))

    def set_destiny(self):
        total = calculate_letter_total(self.name)
        reduced_total_sequence = reduce_and_store_totals(total)
        return Number.get_number_class(parse_sequence(reduced_total_sequence))

    def set_day_of_birth(self):
        birth_date = extract_day_of_birth(self.birthday)
        reduced_birth_sequence = reduce_and_store_totals(birth_date)
        return Number.get_number_class(parse_sequence(reduced_birth_sequence))        

    def set_life_path(self):
        life_path = calculate_number_total(self.birthday)
        reduced_life_sequence = reduce_and_store_totals(life_path)
        return Number.get_number_class(parse_sequence(reduced_life_sequence))

    def set_attitude(self):
        birth_date = extract_day_of_birth(self.birthday)
        birth_month = extrat_month_of_birth(self.birthday)
        attitude_number = calculate_number_total(int(str(birth_date)+str(birth_month)))
        reduced_attitude_sequence = reduce_and_store_totals(attitude_number)
        return Number.get_number_class(parse_sequence(reduced_attitude_sequence))

    # String representation of the object
    def __str__(self):
        return f"Person: {self.name}, Birthday: {self.birthday}, Soul Urge: {self.soul_urge}, " \
               f"Personality: {self.personality}, Destiny: {self.destiny}, Day of Birth: {self.day_of_birth}, " \
               f"Life Path: {self.life_path}, Attitude: {self.attitude}"

    # Formal string representation of the object
    def __repr__(self):
        return f"Person({self.name}, {self.birthday}, {self.soul_urge}, {self.personality}, {self.destiny}, " \
               f"{self.day_of_birth}, {self.life_path}, {self.attitude})"

    def clear_all_fields(self):
        self.name = ""
        self.birthday = ""
        self.soul_urge = zero
        self.personality = zero
        self.destiny = zero
        self.day_of_birth = zero
        self.life_path = zero
        self.attitude = zero

people = []
person = None

def write_variable_to_file(variable):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "inputs.txt")
    # Ensure the file exists before reading
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # Create the file if it does not exist
    with open(file_path, "r") as file:
        lines = file.readlines()
        if variable + "\n" not in lines:
            with open(file_path, "a") as file:
                file.write(variable + "\n")
        # else:
        #     print("Variable already exists in the file.")

def create_numerical_sequence(sequence):
    numerical_sequence = []

    if isinstance(sequence, str):
        for char in sequence:
            if char.isalpha():
                val = ord(char) - 96
                if val > 9:
                    while val > 9:
                        val = sum(map(int, str(val)))
                numerical_sequence.append(val)
            elif char.isdigit():
                numerical_sequence.append(int(char))
    else:
        numerical_sequence = [int(digit) for digit in str(sequence)]

    return numerical_sequence

def has_birthday(input_string):
    pattern = r"\d{4,}"  # Pattern to match four (or more) consecutive digits
    return bool(re.search(pattern, input_string))

def extrat_month_of_birth(input_string):
    return int(input_string[0:2])

def extract_day_of_birth(input_string):
    return int(input_string[2:4])

def exctract_birth_year(input_string):
    pattern = r"\d{4,}"
    return int(re.findall(pattern, input_string)[0][-4:])

def extract_birthday(input_string):
    pattern = r"\d{4,}"
    return int(re.findall(pattern, input_string)[0])

def calculate_letter_total(word):
    return sum((ord(char) - 96) % 9 or 9 for char in word if char.isalpha())

def calculate_number_total(number):
    return sum(int(digit) for digit in str(number))

def reduce_to_single_digit(total):
    total = int(total)
    while len(str(total)) > 1:
        total = sum(int(digit) for digit in str(total))
    return total

def reduce_and_store_totals(total):
    total = int(total)
    intermediate_totals = [total]

    while len(str(total)) > 1:
        total = sum(int(digit) for digit in str(total))
        intermediate_totals.append(total)

    return intermediate_totals

def format_reduced_totals(num_list):
    return ' / '.join(map(str, num_list))

def parse_sequence(sequence):
    return next((num for num in sequence if num in [11, 22, 33]), sequence[-1])

def chinese_zodiac_animal(user_input):
    zodiac_animals = {
        0: ("Rat","Intelligent, Adaptable, and Quick-Witted", ["Dragon", "Monkey"], "Ox", "Horse"),
        1: ("Ox", "Diligent, Dependable, and Strong", ["Snake", "Rooster"], "Rat", "Sheep"),
        2: ("Tiger", "Brave, Confident, and Competitive", ["Horse", "Dog"], "Pig", "Monkey"),
        3: ("Rabbit", "Gentle, Quiet, and Elegant", ["Sheep", "Pig"], "Dog", "Rooster"),
        4: ("Dragon", "Confident, Intelligent, and Enthusiastic", ["Rat", "Monkey"], "Rooster", "Dog"),
        5: ("Snake", "Intelligent, Intuitive, and Elegant", ["Ox", "Rooster"], "Monkey", "Pig"),
        6: ("Horse", "Adaptable, Loyal, and Courageous", ["Tiger", "Dog"], "Sheep", "Rat"),
        7: ("Sheep", "Tasteful, Crafty, and Warm", ["Rabbit", "Pig"], "Horse", "Ox"),
        8: ("Monkey", "Quick-witted, Versatile, and Charming", ["Rat", "Dragon"], "Snake", "Tiger"),
        9: ("Rooster", "Practical, Observant, and Hardworking", ["Ox", "Snake"], "Dragon", "Rabbit"),
        10: ("Dog", "Loyal, Courageous, and Responsible", ["Tiger", "Horse"], "Rabbit", "Dragon"),
        11: ("Pig", "Honorable, Philanthropic, and Sincere", ["Rabbit", "Sheep"], "Tiger", "Snake")
    }

    # The Chinese zodiac cycle starts from 1900 (Year of the Rat)
    start_year = 1900
    birth_year = exctract_birth_year(user_input)
    offset = (birth_year - start_year) % 12

    similar_years = []
    for i in range(-50, 51):
        similar_year = birth_year + i
        similar_offset = (similar_year - start_year) % 12
        if similar_offset == offset:
            similar_years.append(similar_year)

    if similar_years:
        animal, traits, allies, secret_friend, conflict_animal = zodiac_animals[offset]
        print(" Chinese Zodiac ".center(center_val, spacing_symbol))
        print(f"The animal for the year {birth_year} is the {animal}.")
        print(f"Years: {', '.join(map(str, similar_years))}")
        print(f"Traits: {traits}")
        print(f"Allies: {', '.join(allies)}")
        print(f"Secret Friend: {secret_friend}")
        print(f"Conflict Animal: {conflict_animal}")

    else:
        print("Invalid year. Please provide a valid four-digit year.")


def affirmations(user_input):
    print(" Affirmations ".center(center_val, spacing_symbol))
    person.get_life_path().print_health_intro()
    person.get_life_path().print_affirmations()


def attributes(user_input):
	print(" Number Attributes ".center(center_val, spacing_symbol))
	person.get_life_path().print_attributes()

def number_compatability(user_input):
    groups = {
        "Mind Number": [1, 5, 7],
        "Creative Number": [3, 6, 9],
        "Business Number": [2, 4, 8]
    }

    numerical_sequence = create_numerical_sequence(user_input)
    group_counts = {group: sum(numerical_sequence.count(num) for num in nums) for group, nums in groups.items()}
    max_count = max(group_counts.values())
    most_common_groups = [group for group, count in group_counts.items() if count == max_count]

    print(" Number Compatability ".center(center_val, spacing_symbol))
    print(" / ".join(most_common_groups), "Dominant")
    person.get_life_path().print_number_relationships()


def arrows_of_pythagoras(user_input):
    numerical_sequence = create_numerical_sequence(user_input)
    missing_numbers = set(range(1,10)) - set(numerical_sequence) - set(person.get_numbers())

    trios = ['147', '258', '369', '123', '456', '789', '159', '357']
    weaknesses = {
        '147': ('Manual Abilities, Physical Dexterity, Strength, Health',
                'Impracticality, Awkwardness'),
        '258': ('Emotionally Balanced, Artistic, Highly Sensitive',
                'Emotional Confusion, Oversensitivity'),
        '369': ('Intellectual, Creative, Good Judgement',
                'Dullness, Poor Reasoning Ability'),
        '123': ('Good Planning and Organizational Skills, Administrative Abilities, Love of Order',
                'Confusion, Disorder, Lack of Coordination'),
        '456': ('Strong Willpower, Determination to Achieve',
                'Frustration, Disappointment, Sense of Hesitancy'),
        '789': ('Energetic, Enthusiastic, Active',
                'Inertia, Lethargy, Procrastination, Laziness, Apathy'),
        '159': ('Patient, Persistent, Determined, Dogged',
                'Lack of Motivation and Purpose, Resignation, Indecision'),
        '357': ('Compassionate, Spiritually Aware, Serene',
                'Lack of Belief, Poor Spiritual and Emotional Awareness')
    }

    count_dict = {num: numerical_sequence.count(num) for num in set(numerical_sequence)}
    square = [['.' for _ in range(3)] for _ in range(3)]

    for num, freq in count_dict.items():
        if freq > 1:
            for position, val in { (0, 0): '1', (1, 0): '4', (2, 0): '7',
                                   (0, 1): '2', (1, 1): '5', (2, 1): '8',
                                   (0, 2): '3', (1, 2): '6', (2, 2): '9' }.items():
                if val == str(num) and square[position[1]][position[0]] == '.':
                    square[position[1]][position[0]] = str(num) * freq
                    break
        else:
            for position, val in { (0, 0): '1', (1, 0): '4', (2, 0): '7',
                                   (0, 1): '2', (1, 1): '5', (2, 1): '8',
                                   (0, 2): '3', (1, 2): '6', (2, 2): '9' }.items():
                if val == str(num) and square[position[1]][position[0]] == '.':
                    square[position[1]][position[0]] = str(num)
                    break

    print(" Arrows of Pythagoras ".center(center_val, spacing_symbol))

    for row in square[::-1]:
        print(" ".join(row))

    if missing_numbers:
        #missing_numbers -= set(person.get_numbers())
        print("Missing Numbers:", missing_numbers)

    for trio in trios:

        description = weaknesses[trio]
        if any(int(num) in missing_numbers for num in trio):
            description = description[1]  # Incomplete
        else:
            description = description[0]
        
        if missing_numbers.intersection(map(int, trio)):
            print(trio, "INCOMPLETE:", description)
        #else:
            #print(trio, "Complete:", description)


def process_full_birthday(birthday):
    if len(str(birthday)) < 8:
        birth_date = extract_day_of_birth("0"+str(birthday))
        birth_month = extrat_month_of_birth("0"+str(birthday))
    else:
        birth_date = extract_day_of_birth(str(birthday))
        birth_month = extrat_month_of_birth(str(birthday))
    
    reduced_birth_sequence = reduce_and_store_totals(birth_date)
    print("Day of Birth Number - Natural Disposition:", 
        format_reduced_totals(reduced_birth_sequence))
    person.get_day_of_birth().print_numerology_characteristics()

    life_path = calculate_number_total(birthday)
    reduced_life_sequence = reduce_and_store_totals(life_path)
    print("Life Path Number - To Fulfill Life's Purpose:", 
        format_reduced_totals(reduced_life_sequence))
    person.get_life_path().print_numerology_characteristics()

    attitude_number = calculate_number_total(int(str(birth_date)+str(birth_month)))
    reduced_attitude_sequence = reduce_and_store_totals(attitude_number)
    print("Achievement Number - General Attitude Toward Life:", 
        format_reduced_totals(reduced_attitude_sequence))
    person.get_attitude().print_numerology_characteristics()


def calculate_phrase_numerology(user_input):
    print(" Numerology Analysis ".center(center_val, spacing_symbol))  

    vowel_total = calculate_letter_total(filter(lambda x: x in "aeiou", user_input))
    reduced_vowel_sequence = reduce_and_store_totals(vowel_total)
    print("Soul Urge Number - How You Feel Deep Down:", 
        format_reduced_totals(reduced_vowel_sequence))
    person.get_soul_urge().print_numerology_characteristics()

    consonant_total = calculate_letter_total(filter(lambda x: x in "bcdfghjklmnpqrstvwxyz", user_input))
    reduced_consonant_sequence = reduce_and_store_totals(consonant_total)
    print("Personality Number - How People Will Precieve You:", 
        format_reduced_totals(reduced_consonant_sequence))
    person.get_personality().print_numerology_characteristics()

    total = calculate_letter_total(user_input)
    reduced_total_sequence = reduce_and_store_totals(total)
    print("Destiny Number - Power of Your Name:", 
        format_reduced_totals(reduced_total_sequence))
    person.get_destiny().print_numerology_characteristics()

    if has_birthday(user_input):
        birthday = extract_birthday(user_input)
        process_full_birthday(birthday)


def process_digit_input(user_input):
    reduction = Number.get_number_class(reduce_to_single_digit(user_input))
    print(user_input, "reduces down to ", reduction.get_value())
    reduction.print_numerology_characteristics()
    print(" Number Compatability ".center(center_val, spacing_symbol))
    reduction.print_number_relationships()


def process_data(user_input):
    buffer = io.StringIO()
    global person

    with redirect_stdout(buffer):
        print("Numerology Calculator V2.0:", user_input)
        write_variable_to_file(user_input)
        
        name = ''.join(char for char in user_input if char.isalpha())
        birthday = ''.join(char for char in user_input if char.isdigit())
        person = Person(name, birthday)
        people.append(person)

        if user_input.isdigit():
            print(" Numerology Analysis ".center(center_val, spacing_symbol))
            
            if len(str(user_input)) != 8:
                process_digit_input(user_input)
                
                if len(str(user_input)) == 4:
                    chinese_zodiac_animal(user_input)

            else:
                process_full_birthday(user_input)
                arrows_of_pythagoras(user_input)
                number_compatability(user_input)
                attributes(user_input)
                affirmations(user_input)
                chinese_zodiac_animal(user_input)

        else:
            calculate_phrase_numerology(user_input)
            arrows_of_pythagoras(user_input)
            number_compatability(user_input)
            attributes(user_input)
            affirmations(user_input)
            
            if has_birthday(user_input):
                chinese_zodiac_animal(user_input)
        
        print("".center(center_val, spacing_symbol))
        person.clear_all_fields()
    output = buffer.getvalue()
    return output

