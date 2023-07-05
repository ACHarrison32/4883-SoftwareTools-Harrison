```cpp
import csv
import datetime
########################################################################################
#                            Assign a color to each clan                               #
########################################################################################
color_map = {
    'Oakenheart': 'purple',
    'Silverwood': 'green',
    'Thornfield': 'yellow',
    'Blackthorn': 'orange',
    'Brazenbush': 'red',
    'Ironhammer': 'pink',
}
########################################################################################
#                Function to get the color code based on the clan name                 #
########################################################################################
def get_clan_color(clan):
    if clan in color_map:
        return color_map[clan]
    else:
        return 'lightgray'  # Default color for unknown clans
########################################################################################
#           Class for Person that represents an individual in the family tree          #
########################################################################################
class Person:
    def __init__(
        self,
        pid,
        first_name,
        last_name,
        gender,
        birth_year,
        death_year=None,
        spouse_id=None,
        parent_id1=None,
        parent_id2=None,
        clan=None,
        generation=None,
    ):
        self.pid = pid
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_year = birth_year
        self.death_year = death_year
        self.spouse_id = spouse_id
        self.parent_id1 = parent_id1
        self.parent_id2 = parent_id2
        self.clan = clan
        self.generation = generation
        self.children = []
########################################################################################
#           Method definition in the Person class to add a child to the list           #
#                                     of children                                      #
########################################################################################
    def add_child(self, child):
        self.children.append(child)
########################################################################################
#             Function for calculating the age based on the birth year and             #
#                                     death year                                       #
########################################################################################
def calculate_age(birth_year, death_year=None):
    current_year = datetime.datetime.now().year
    if death_year is None:
        return current_year - birth_year
    else:
        return death_year - birth_year
########################################################################################
#          Recursively generates the family tree graph using DOT syntax based          #
#              on the provided person and writes the graph to a dot_file.              #
#         Generates the label and shape for the current person and writes the          #
#                   corresponding node declaration to the dot_file.                    #
########################################################################################
def generate_family_tree(person, dot_file):
    name = f"{person.first_name} {person.last_name}"
    birth_year = person.birth_year
    death_year = person.death_year or "Still Alive"
    age = calculate_age(birth_year, person.death_year)
    clan_color = get_clan_color(person.clan)
########################################################################################
#                   Generates the HTML-like label for the person                       #
########################################################################################
    label = f'<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="{clan_color}"><b>{name}</b></td></tr>'
    label += f'<tr><td>Gender: {person.gender}</td></tr>'
    label += f'<tr><td>{birth_year} - {death_year}</td></tr>'
    label += f'<tr><td>Age: {age}</td></tr>'
    label += f'<tr><td>Clan: {person.clan}</td></tr>'
    label += f'<tr><td>Gen: {person.generation}</td></tr></table>>'

    dot_file.write(f'\t{person.pid} [label={label}, shape=rectangle];\n')
########################################################################################
#          If the person has a spouse, retrieve the spouse information and             #  
#                       generate the spouse node declaration.                          #
########################################################################################
    if person.spouse_id is not None:
        spouse = people[person.spouse_id]
        spouse_name = f"{spouse.first_name} {spouse.last_name}"
        spouse_birth_year = spouse.birth_year
        spouse_death_year = spouse.death_year or "Still Alive"
        spouse_age = calculate_age(spouse_birth_year, spouse.death_year)
        spouse_clan_color = get_clan_color(spouse.clan)
########################################################################################
#                   Generates the HTML-like label for the spouse                       #
########################################################################################
        spouse_label = f'<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="{spouse_clan_color}"><b>{spouse_name}</b></td></tr>'
        spouse_label += f'<tr><td>Gender: {spouse.gender}</td></tr>'
        spouse_label += f'<tr><td>{spouse_birth_year} - {spouse_death_year}</td></tr>'
        spouse_label += f'<tr><td>Age: {spouse_age}</td></tr>'
        spouse_label += f'<tr><td>Clan: {spouse.clan}</td></tr>'
        spouse_label += f'<tr><td>Gen: {spouse.generation}</td></tr></table>>'

        dot_file.write(f'\t{person.pid} -> {person.spouse_id} [label="Spouse", dir=none, penwidth=2, color="blue"];\n')
        dot_file.write(f'\t{person.spouse_id} [label={spouse_label}, shape=rectangle];\n')
########################################################################################
#      Recursively generate the family tree for each child of the current person.      #
########################################################################################
    for child in person.children:
        dot_file.write(f'\t{person.pid} -> {child.pid}[penwidth=2];\n')
        generate_family_tree(child, dot_file)
########################################################################################
#                              Read input data from CSV file                           #
#         Creates an empty dictionary called people to store the Person objects        #
########################################################################################
people = {}
########################################################################################
#               Opens the CSV file in read mode and creates a CSV reader.              #
########################################################################################
with open('family_tree_data.csv', 'r') as file:
    reader = csv.DictReader(file)
########################################################################################
#     Iterates over each row in the CSV file and extracts the values for various       #
#                               attributes of a Person.                                #
########################################################################################
    for row in reader:
        pid = int(row['pid'])
        first_name = row['firstName']
        last_name = row['lastName']
        gender = row['gender']
        birth_year = int(row['byear'])
        death_year = None if row['dyear'] == '' else int(row['dyear'])
        spouse_id = None if row['spouseId'] == '' else int(row['spouseId'])
        parent_id1 = None if row['parentId1'] == '' else int(row['parentId1'])
        parent_id2 = None if row['parentId2'] == '' else int(row['parentId2'])
        clan = row['clan']
        generation = int(row['generation'])
########################################################################################
#       Creates a new Person object with the extracted values and adds it to the       #
#                    people dictionary using the person's ID as the key.               #
########################################################################################
        person = Person(
            pid,
            first_name,
            last_name,
            gender,
            birth_year,
            death_year,
            spouse_id,
            parent_id1,
            parent_id2,
            clan,
            generation,
        )
        people[pid] = person

########################################################################################
#       Build relationships between people and determine the maximum generation        #
########################################################################################
max_generation = 0
for person in people.values():
########################################################################################
#         For each person, if they have a parent ID 1, retrieve the parent 1           #
#                      object and add the person as their child.                       #
########################################################################################
    if person.parent_id1 is not None:
        parent1 = people[person.parent_id1]
        parent1.add_child(person)
        max_generation = max(max_generation, parent1.generation + 1)
########################################################################################
#         If the person has a parent ID 2, retrieve the parent 2 object and add        #
#                             the person as their child.                               #
########################################################################################
    if person.parent_id2 is not None:
        parent2 = people[person.parent_id2]
        parent2.add_child(person)
        max_generation = max(max_generation, parent2.generation + 1)
########################################################################################
#                                Generate the DOT file                                 #
########################################################################################
dot_filename = 'family_tree.dot'
with open(dot_filename, 'w') as dot_file:
########################################################################################
#     Writes the initial line to start the declaration of the family tree graph.       #
########################################################################################
    dot_file.write('digraph FamilyTree {\n')
########################################################################################
#                    Generate the family tree graph for each generation                #
########################################################################################
    for generation in range(max_generation + 1):
        dot_file.write(f'\t{{ rank = same; ')
        for person in people.values():
            if person.generation == generation:
                dot_file.write(f'{person.pid}; ')
        dot_file.write('}\n')
########################################################################################
#          Retrieves the root node (person with ID 0) from the people dictionary.      #
########################################################################################
    root_node = people[0]
########################################################################################
#       Calls the generate_family_tree function with the root node and the DOT file    #
#                 object to generate the family tree graph recursively.                #
########################################################################################
    generate_family_tree(root_node, dot_file)
    dot_file.write('}\n')

print(f"DOT file '{dot_filename}' generated successfully.")
```
