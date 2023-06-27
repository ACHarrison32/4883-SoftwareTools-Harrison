# A05 - Creating a Family Tree using python and graphviz

### Description:
#### produce a family tree graph generated using GraphViz and also done programmatically, meaning, you do not create the graph by hand, you use a programming language and (optionally) a library to generate the dot file for the graph.

## Family Tree Generated
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A5/Family_Tree_Graphviz.png">

## Python code used to make the dot file
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

## Dot file created from the Python code
```cpp
digraph FamilyTree {
	{ rank = same; }
	{ rank = same; 0; 1; }
	{ rank = same; 2; 3; 26; 33; }
	{ rank = same; 4; 5; 34; 35; }
	{ rank = same; 6; 7; 8; 9; 10; 36; 37; 38; }
	{ rank = same; 11; 12; 13; 14; 27; 28; 39; }
	{ rank = same; 15; 16; 17; 18; 19; 29; 30; 40; 41; }
	{ rank = same; 20; 21; 24; 31; 32; 42; 43; 47; }
	{ rank = same; 22; 23; 44; 45; 46; 48; 49; 50; 51; }
	{ rank = same; 25; 52; }
	0 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Jack Stallings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1800 - 1869</td></tr><tr><td>Age: 69</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 1</td></tr></table>>, shape=rectangle];
	0 -> 1 [label="Spouse", dir=none, penwidth=2, color="blue"];
	1 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Allison Stallings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1803 - 1897</td></tr><tr><td>Age: 94</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 1</td></tr></table>>, shape=rectangle];
	0 -> 2[penwidth=2];
	2 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Nicole Stallings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1821 - 1876</td></tr><tr><td>Age: 55</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 2</td></tr></table>>, shape=rectangle];
	2 -> 3 [label="Spouse", dir=none, penwidth=2, color="blue"];
	3 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Steven Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1819 - 1862</td></tr><tr><td>Age: 43</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 2</td></tr></table>>, shape=rectangle];
	2 -> 4[penwidth=2];
	4 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Jack Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1849 - 1910</td></tr><tr><td>Age: 61</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 3</td></tr></table>>, shape=rectangle];
	4 -> 5 [label="Spouse", dir=none, penwidth=2, color="blue"];
	5 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Patricia Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1856 - 1926</td></tr><tr><td>Age: 70</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 3</td></tr></table>>, shape=rectangle];
	4 -> 6[penwidth=2];
	6 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Denise Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1886 - 1963</td></tr><tr><td>Age: 77</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	6 -> 27[penwidth=2];
	27 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Shiela Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1915 - 2000</td></tr><tr><td>Age: 85</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	27 -> 28 [label="Spouse", dir=none, penwidth=2, color="blue"];
	28 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Robert Harrison</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1910 - 2002</td></tr><tr><td>Age: 92</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	27 -> 29[penwidth=2];
	29 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Christopher Harrison</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1937 - 2015</td></tr><tr><td>Age: 78</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	29 -> 30 [label="Spouse", dir=none, penwidth=2, color="blue"];
	30 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Tammy Harrison</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1940 - 2021</td></tr><tr><td>Age: 81</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	29 -> 31[penwidth=2];
	31 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Andrew Harrison</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1977 - Still Alive</td></tr><tr><td>Age: 46</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	31 -> 32 [label="Spouse", dir=none, penwidth=2, color="blue"];
	32 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Paige Harrison</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1978 - Still Alive</td></tr><tr><td>Age: 45</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	31 -> 48[penwidth=2];
	48 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Ezekiel Harrison</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1999 - Still Alive</td></tr><tr><td>Age: 24</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	31 -> 49[penwidth=2];
	49 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Bartholomew Harrison</b></td></tr><tr><td>Gender: M</td></tr><tr><td>2002 - Still Alive</td></tr><tr><td>Age: 21</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	31 -> 50[penwidth=2];
	50 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="pink"><b>Charolette Harrison</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1997 - Still Alive</td></tr><tr><td>Age: 26</td></tr><tr><td>Clan: Ironhammer</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	50 -> 51 [label="Spouse", dir=none, penwidth=2, color="blue"];
	51 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="pink"><b>Jerimiah Jefferies</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1997 - Still Alive</td></tr><tr><td>Age: 26</td></tr><tr><td>Clan: Ironhammer</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	50 -> 52[penwidth=2];
	52 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="pink"><b>Elizabeth Jefferies</b></td></tr><tr><td>Gender: F</td></tr><tr><td>2023 - Still Alive</td></tr><tr><td>Age: 0</td></tr><tr><td>Clan: Ironhammer</td></tr><tr><td>Gen: 9</td></tr></table>>, shape=rectangle];
	29 -> 47[penwidth=2];
	47 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="red"><b>Peter Harrison</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1979 - Still Alive</td></tr><tr><td>Age: 44</td></tr><tr><td>Clan: Brazenbush</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	4 -> 7[penwidth=2];
	7 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Bruce Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1886 - 1962</td></tr><tr><td>Age: 76</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	4 -> 8[penwidth=2];
	8 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Richard Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1888 - 1902</td></tr><tr><td>Age: 14</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	4 -> 9[penwidth=2];
	9 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Travis Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1890 - 1981</td></tr><tr><td>Age: 91</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	9 -> 10 [label="Spouse", dir=none, penwidth=2, color="blue"];
	10 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Kelly Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1887 - 1950</td></tr><tr><td>Age: 63</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	9 -> 11[penwidth=2];
	11 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Daniel Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1921 - 2001</td></tr><tr><td>Age: 80</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	11 -> 12 [label="Spouse", dir=none, penwidth=2, color="blue"];
	12 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Sheila Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1924 - 2015</td></tr><tr><td>Age: 91</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	11 -> 15[penwidth=2];
	15 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Charles Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1947 - 2000</td></tr><tr><td>Age: 53</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	15 -> 16 [label="Spouse", dir=none, penwidth=2, color="blue"];
	16 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Jane Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1960 - 2021</td></tr><tr><td>Age: 61</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	15 -> 24[penwidth=2];
	24 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="green"><b>Emma Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>2000 - Still Alive</td></tr><tr><td>Age: 23</td></tr><tr><td>Clan: Silverwood</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	11 -> 17[penwidth=2];
	17 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Daniella Flemmings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1922 - Still Alive</td></tr><tr><td>Age: 101</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	17 -> 18 [label="Spouse", dir=none, penwidth=2, color="blue"];
	18 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Joshua Richardson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1952 - Still Alive</td></tr><tr><td>Age: 71</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	17 -> 20[penwidth=2];
	20 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Joseph Richardson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1977 - Still Alive</td></tr><tr><td>Age: 46</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	20 -> 21 [label="Spouse", dir=none, penwidth=2, color="blue"];
	21 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Elaine Richardson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1977 - Still Alive</td></tr><tr><td>Age: 46</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	20 -> 22[penwidth=2];
	22 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Eric Richardson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1999 - Still Alive</td></tr><tr><td>Age: 24</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	22 -> 23 [label="Spouse", dir=none, penwidth=2, color="blue"];
	23 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Edith Richardson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>2000 - Still Alive</td></tr><tr><td>Age: 23</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	22 -> 25[penwidth=2];
	25 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="orange"><b>Craig Richardson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>2022 - Still Alive</td></tr><tr><td>Age: 1</td></tr><tr><td>Clan: Blackthorn</td></tr><tr><td>Gen: 9</td></tr></table>>, shape=rectangle];
	9 -> 13[penwidth=2];
	13 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Pamela Flemmings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1923 - 2020</td></tr><tr><td>Age: 97</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	13 -> 14 [label="Spouse", dir=none, penwidth=2, color="blue"];
	14 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Clifford Johnson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1910 - 2002</td></tr><tr><td>Age: 92</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	13 -> 19[penwidth=2];
	19 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Anita Johnson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1950 - 1955</td></tr><tr><td>Age: 5</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	13 -> 40[penwidth=2];
	40 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Martin Johnson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1953 - 2003</td></tr><tr><td>Age: 50</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	40 -> 41 [label="Spouse", dir=none, penwidth=2, color="blue"];
	41 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Meradith Johnson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1957 - 2022</td></tr><tr><td>Age: 65</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 6</td></tr></table>>, shape=rectangle];
	40 -> 42[penwidth=2];
	42 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Kalyb Johnson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1977 - Still Alive</td></tr><tr><td>Age: 46</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	42 -> 43 [label="Spouse", dir=none, penwidth=2, color="blue"];
	43 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Mariya Johnson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1978 - Still Alive</td></tr><tr><td>Age: 45</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 7</td></tr></table>>, shape=rectangle];
	42 -> 44[penwidth=2];
	44 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Jiriya Johnson</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1999 - Still Alive</td></tr><tr><td>Age: 24</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	42 -> 45[penwidth=2];
	45 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Sara Johnson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1999 - Still Alive</td></tr><tr><td>Age: 24</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	42 -> 46[penwidth=2];
	46 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="yellow"><b>Whitney Johnson</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1999 - Still Alive</td></tr><tr><td>Age: 24</td></tr><tr><td>Clan: Thornfield</td></tr><tr><td>Gen: 8</td></tr></table>>, shape=rectangle];
	0 -> 26[penwidth=2];
	26 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Jim Stallings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1825 - 1891</td></tr><tr><td>Age: 66</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 2</td></tr></table>>, shape=rectangle];
	26 -> 33 [label="Spouse", dir=none, penwidth=2, color="blue"];
	33 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Amy Stallings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1826 - 1893</td></tr><tr><td>Age: 67</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 2</td></tr></table>>, shape=rectangle];
	26 -> 34[penwidth=2];
	34 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Greg Stallings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1852 - 1921</td></tr><tr><td>Age: 69</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 3</td></tr></table>>, shape=rectangle];
	34 -> 35 [label="Spouse", dir=none, penwidth=2, color="blue"];
	35 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Landry Stallings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1855 - 1945</td></tr><tr><td>Age: 90</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 3</td></tr></table>>, shape=rectangle];
	34 -> 36[penwidth=2];
	36 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Matt Stallings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1887 - 1967</td></tr><tr><td>Age: 80</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	36 -> 37 [label="Spouse", dir=none, penwidth=2, color="blue"];
	37 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Maddison Stallings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1887 - 1972</td></tr><tr><td>Age: 85</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
	36 -> 39[penwidth=2];
	39 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Jimmy Stallings</b></td></tr><tr><td>Gender: M</td></tr><tr><td>1923 - 1925</td></tr><tr><td>Age: 2</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 5</td></tr></table>>, shape=rectangle];
	34 -> 38[penwidth=2];
	38 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="4"><tr><td bgcolor="purple"><b>Leslie Stallings</b></td></tr><tr><td>Gender: F</td></tr><tr><td>1887 - 1945</td></tr><tr><td>Age: 58</td></tr><tr><td>Clan: Oakenheart</td></tr><tr><td>Gen: 4</td></tr></table>>, shape=rectangle];
}
```

### Family Tree Data in the csv file
```dot
pid,firstName,lastName,gender,byear,dyear,dage,spouseId,parentId1,parentId2,clan,generation
0,Jack,Stallings,M,1800,1869,69,1,,,Oakenheart,1
1,Allison,Stallings,F,1803,1897,94,0,,,Oakenheart,1
2,Nicole,Stallings,F,1821,1876,55,3,0,1,Silverwood,2
3,Steven,Flemmings,M,1819,1862,43,2,,,Silverwood,2
4,Jack,Flemmings,M,1849,1910,61,5,2,3,Silverwood,3
5,Patricia,Flemmings,F,1856,1926,70,4,,,Silverwood,3
6,Denise,Flemmings,F,1886,1963,77,,4,5,Silverwood,4
7,Bruce,Flemmings,M,1886,1962,76,,4,5,Silverwood,4
8,Richard,Flemmings,M,1888,1902,14,,4,5,Silverwood,4
9,Travis,Flemmings,M,1890,1981,91,10,4,5,Silverwood,4
10,Kelly,Flemmings,F,1887,1950,63,9,,,Silverwood,4
11,Daniel,Flemmings,M,1921,2001,80,12,9,10,Silverwood,5
12,Sheila,Flemmings,F,1924,2015,91,11,,,Silverwood,5
13,Pamela,Flemmings,F,1923,2020,97,14,9,10,Thornfield,5
14,Clifford,Johnson,M,1910,2002,92,13,,,Thornfield,5
15,Charles,Flemmings,M,1947,2000,53,16,11,12,Silverwood,6
16,Jane,Flemmings,F,1960,2021,61,15,,,Silverwood,6
17,Daniella,Flemmings,M,1922,,74,18,11,12,Blackthorn,6
18,Joshua,Richardson,M,1952,,71,17,,,Blackthorn,6
19,Anita,Johnson,F,1950,1955,5,,13,14,Thornfield,6
20,Joseph,Richardson,M,1977,,46,21,17,18,Blackthorn,7
21,Elaine,Richardson,F,1977,,46,20,,,Blackthorn,7
22,Eric,Richardson,M,1999,,23,23,20,21,Blackthorn,8
23,Edith,Richardson,F,2000,,23,22,,,Blackthorn,8
24,Emma,Flemmings,F,2000,,23,,15,16,Silverwood,7
25,Craig,Richardson,M,2022,,1,,22,23,Blackthorn,9
26,Jim,Stallings,M,1825,1891,66,33,0,1,Oakenheart,2
27,Shiela,Flemmings,F,1915,2000,85,28,6,,Brazenbush,5
28,Robert,Harrison,M,1910,2002,92,27,,,Brazenbush,5
29,Christopher,Harrison,M,1937,2015,78,30,27,28,Brazenbush,6
30,Tammy,Harrison,F,1940,2021,81,29,,,Brazenbush,6
31,Andrew,Harrison,M,1977,,46,32,29,30,Brazenbush,7
32,Paige,Harrison,F,1978,,45,31,,,Brazenbush,7
33,Amy,Stallings,F,1826,1893,67,26,,,Oakenheart,2
34,Greg,Stallings,M,1852,1921,69,35,26,33,Oakenheart,3
35,Landry,Stallings,F,1855,1945,90,34,,,Oakenheart,3
36,Matt,Stallings,M,1887,1967,80,37,34,35,Oakenheart,4
37,Maddison,Stallings,F,1887,1972,85,36,,,Oakenheart,4
38,Leslie,Stallings,F,1887,1945,58,,34,35,Oakenheart,4
39,Jimmy,Stallings,M,1923,1925,2,,37,36,Oakenheart,5
40,Martin,Johnson,M,1953,2003,50,41,13,14,Thornfield,6
41,Meradith,Johnson,F,1957,2022,65,40,,,Thornfield,6
42,Kalyb,Johnson,M,1977,,46,43,40,41,Thornfield,7
43,Mariya,Johnson,F,1978,,45,42,,,Thornfield,7
44,Jiriya,Johnson,M,1999,,,,42,43,Thornfield,8
45,Sara,Johnson,F,1999,,,,42,43,Thornfield,8
46,Whitney,Johnson,F,1999,,,,42,43,Thornfield,8
47,Peter,Harrison,M,1979,,44,,29,30,Brazenbush,7
48,Ezekiel,Harrison,M,1999,,23,,31,32,Brazenbush,8
49,Bartholomew,Harrison,M,2002,,,,31,32,Brazenbush,8
50,Charolette,Harrison,F,1997,,,51,31,32,Ironhammer,8
51,Jerimiah,Jefferies,M,1997,,,50,,,Ironhammer,8
52,Elizabeth,Jefferies,F,2023,,,,50,51,Ironhammer,9
```
