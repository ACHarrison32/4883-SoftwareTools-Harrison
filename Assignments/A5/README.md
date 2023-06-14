# Assignment 5 - Creating a Family Tree using python and graphviz

### Family Tree Generated
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A5/Family_Tree.png">

### Python code used to make the dot file
```cpp
# Andrew Harrison
# 06/13/2023
# Assignment 5 - Family Tree
# Professor Griffin - 4883 Software Tools
import csv
import datetime

# Define color assignments for different clans
color_map = {
  'Oakenheart': 'purple',
  'Silverwood': 'green',
  'Thornfield': 'yellow',
  'Blackthorn': 'orange',
  'Brazenbush': 'red',
  'Ironhammer': 'pink',
  # Add more clan-color mappings here
}


# Function to get the color code based on the clan name
def get_clan_color(clan):
  if clan in color_map:
    return color_map[clan]
  else:
    return 'lightgray'  # Default color for unknown clans


# Defines a class Person that represents an individual in the family 
# tree
class Person:
  def __init__(self,
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
               generation=None):
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

  # Defines a method in the Person class to add a child to the list 
  # of children.
  def add_child(self, child):
    self.children.append(child)


# Defines a function calculate_age that calculates the age based on 
# the birth year and death year (if provided).
def calculate_age(birth_year, death_year=None):
  current_year = datetime.datetime.now().year
  if death_year is None:
    return current_year - birth_year
  else:
    return death_year - birth_year


# Recursively generates the family tree graph using DOT syntax based 
# on the provided person and writes the graph to a dot_file.
# Generates the label and shape for the current person and writes the 
# corresponding node declaration to the dot_file.
def generate_family_tree(person, dot_file):
  name = f"{person.first_name} {person.last_name}"
  birth_year = person.birth_year
  death_year = person.death_year or "Still Alive"
  age = calculate_age(birth_year, person.death_year)
  clan_color = get_clan_color(person.clan)
  label = f"{name}\\n{birth_year} - {death_year}\\nAge: {age}\\nClan: {person.clan}\\nGen: {person.generation}"
  dot_file.write(f'\t{person.pid} [label="{label}", shape=rectangle, style=filled, fillcolor={clan_color}];\n')
  # If the person has a spouse, it retrieves the spouse information, generates
  # the label and shape, and writes the spouse node declaration and the spouse
  # connection to the dot_file.
  if person.spouse_id is not None:
    spouse = people[person.spouse_id]
    spouse_name = f"{spouse.first_name} {spouse.last_name}"
    spouse_birth_year = spouse.birth_year
    spouse_death_year = spouse.death_year or "Still Alive"
    spouse_age = calculate_age(spouse_birth_year, spouse.death_year)
    spouse_clan_color = get_clan_color(spouse.clan)
    spouse_label = f"{spouse_name}\\n{spouse_birth_year} - {spouse_death_year}\\nAge: {spouse_age}\\nClan: {spouse.clan}\\nGen:{spouse.generation}"
    dot_file.write(f'\t{person.pid} -> {person.spouse_id} [label="Spouse", dir=none, penwidth=2, color="blue"];\n')
    dot_file.write(f'\t{person.spouse_id} [label="{spouse_label}", shape=rectangle, style=filled, fillcolor={spouse_clan_color}];\n')
  # Recursively generates the family tree for each child of the current person.
  for child in person.children:
    dot_file.write(f'\t{person.pid} -> {child.pid}[penwidth=2];\n')
    generate_family_tree(child, dot_file)

# Read input data from CSV file
# Creates an empty dictionary people to store Person objects.
people = {}
# Opens the 'family_tree_data.csv' file in read mode and creates a CSV reader.
with open('family_tree_data.csv', 'r') as file:
  reader = csv.DictReader(file)
  # Iterates over each row in the CSV file and extracts the values for various
  # attributes of a Person.
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
    # Creates a new Person object with the extracted values and adds it to the
    # people dictionary using the person's ID as the key.
    person = Person(pid, first_name, last_name, gender, birth_year, death_year,spouse_id, parent_id1, parent_id2, clan, generation)
    people[pid] = person

# Build relationships between people and determine the maximum generation
max_generation = 0
for person in people.values():
  # For each person, if they have a parent ID 1, it retrieves the parent 1
  # object and adds the person as their child.
  if person.parent_id1 is not None:
    parent1 = people[person.parent_id1]
    parent1.add_child(person)
    max_generation = max(max_generation, parent1.generation + 1)
  # If the person has a parent ID 2, it retrieves the parent 2 object and adds
  # the person as their child.
  if person.parent_id2 is not None:
    parent2 = people[person.parent_id2]
    parent2.add_child(person)
    max_generation = max(max_generation, parent2.generation + 1)

# Generate the DOT file
dot_filename = 'family_tree.dot'
with open(dot_filename, 'w') as dot_file:
  # Writes the initial line to start the declaration of the family tree graph.
  dot_file.write('digraph FamilyTree {\n')
  # Generate the family tree graph for each generation
  for generation in range(max_generation + 1):
    dot_file.write(f'\t{{ rank = same; ')
    for person in people.values():
      if person.generation == generation:
        dot_file.write(f'{person.pid}; ')
    dot_file.write('}\n')
  # Retrieves the root node (person with ID 0) from the people dictionary.
  root_node = people[0]
  # Calls the generate_family_tree function with the root node and the DOT file
  # object to generate the family tree graph recursively.
  generate_family_tree(root_node, dot_file)
  dot_file.write('}\n')

print(f"DOT file '{dot_filename}' generated successfully.")
```

### Dot file created from the Python code
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
	0 [label="Jack Stallings\n1800 - 1869\nAge: 69\nClan: Oakenheart\nGen: 1", shape=rectangle, style=filled, fillcolor=purple];
	0 -> 1 [label="Spouse", dir=none, penwidth=2, color="blue"];
	1 [label="Allison Stallings\n1803 - 1897\nAge: 94\nClan: Oakenheart\nGen:1", shape=rectangle, style=filled, fillcolor=purple];
	0 -> 2[penwidth=2];
	2 [label="Nicole Stallings\n1821 - 1876\nAge: 55\nClan: Silverwood\nGen: 2", shape=rectangle, style=filled, fillcolor=green];
	2 -> 3 [label="Spouse", dir=none, penwidth=2, color="blue"];
	3 [label="Steven Flemmings\n1819 - 1862\nAge: 43\nClan: Silverwood\nGen:2", shape=rectangle, style=filled, fillcolor=green];
	2 -> 4[penwidth=2];
	4 [label="Jack Flemmings\n1849 - 1910\nAge: 61\nClan: Silverwood\nGen: 3", shape=rectangle, style=filled, fillcolor=green];
	4 -> 5 [label="Spouse", dir=none, penwidth=2, color="blue"];
	5 [label="Patricia Flemmings\n1856 - 1926\nAge: 70\nClan: Silverwood\nGen:3", shape=rectangle, style=filled, fillcolor=green];
	4 -> 6[penwidth=2];
	6 [label="Denise Flemmings\n1886 - 1963\nAge: 77\nClan: Silverwood\nGen: 4", shape=rectangle, style=filled, fillcolor=green];
	6 -> 27[penwidth=2];
	27 [label="Shiela Flemmings\n1915 - 2000\nAge: 85\nClan: Brazenbush\nGen: 5", shape=rectangle, style=filled, fillcolor=red];
	27 -> 28 [label="Spouse", dir=none, penwidth=2, color="blue"];
	28 [label="Robert Harrison\n1910 - 2002\nAge: 92\nClan: Brazenbush\nGen:5", shape=rectangle, style=filled, fillcolor=red];
	27 -> 29[penwidth=2];
	29 [label="Christopher Harrison\n1937 - 2015\nAge: 78\nClan: Brazenbush\nGen: 6", shape=rectangle, style=filled, fillcolor=red];
	29 -> 30 [label="Spouse", dir=none, penwidth=2, color="blue"];
	30 [label="Tammy Harrison\n1940 - 2021\nAge: 81\nClan: Brazenbush\nGen:6", shape=rectangle, style=filled, fillcolor=red];
	29 -> 31[penwidth=2];
	31 [label="Andrew Harrison\n1977 - Still Alive\nAge: 46\nClan: Brazenbush\nGen: 7", shape=rectangle, style=filled, fillcolor=red];
	31 -> 32 [label="Spouse", dir=none, penwidth=2, color="blue"];
	32 [label="Paige Harrison\n1978 - Still Alive\nAge: 45\nClan: Brazenbush\nGen:7", shape=rectangle, style=filled, fillcolor=red];
	31 -> 48[penwidth=2];
	48 [label="Ezekiel Harrison\n1999 - Still Alive\nAge: 24\nClan: Brazenbush\nGen: 8", shape=rectangle, style=filled, fillcolor=red];
	31 -> 49[penwidth=2];
	49 [label="Bartholomew Harrison\n2002 - Still Alive\nAge: 21\nClan: Brazenbush\nGen: 8", shape=rectangle, style=filled, fillcolor=red];
	31 -> 50[penwidth=2];
	50 [label="Charolette Harrison\n1997 - Still Alive\nAge: 26\nClan: Ironhammer\nGen: 8", shape=rectangle, style=filled, fillcolor=pink];
	50 -> 51 [label="Spouse", dir=none, penwidth=2, color="blue"];
	51 [label="Jerimiah Jefferies\n1997 - Still Alive\nAge: 26\nClan: Ironhammer\nGen:8", shape=rectangle, style=filled, fillcolor=pink];
	50 -> 52[penwidth=2];
	52 [label="Elizabeth Jefferies\n2023 - Still Alive\nAge: 0\nClan: Ironhammer\nGen: 9", shape=rectangle, style=filled, fillcolor=pink];
	29 -> 47[penwidth=2];
	47 [label="Peter Harrison\n1979 - Still Alive\nAge: 44\nClan: Brazenbush\nGen: 7", shape=rectangle, style=filled, fillcolor=red];
	4 -> 7[penwidth=2];
	7 [label="Bruce Flemmings\n1886 - 1962\nAge: 76\nClan: Silverwood\nGen: 4", shape=rectangle, style=filled, fillcolor=green];
	4 -> 8[penwidth=2];
	8 [label="Richard Flemmings\n1888 - 1902\nAge: 14\nClan: Silverwood\nGen: 4", shape=rectangle, style=filled, fillcolor=green];
	4 -> 9[penwidth=2];
	9 [label="Travis Flemmings\n1890 - 1981\nAge: 91\nClan: Silverwood\nGen: 4", shape=rectangle, style=filled, fillcolor=green];
	9 -> 10 [label="Spouse", dir=none, penwidth=2, color="blue"];
	10 [label="Kelly Flemmings\n1887 - 1950\nAge: 63\nClan: Silverwood\nGen:4", shape=rectangle, style=filled, fillcolor=green];
	9 -> 11[penwidth=2];
	11 [label="Daniel Flemmings\n1921 - 2001\nAge: 80\nClan: Silverwood\nGen: 5", shape=rectangle, style=filled, fillcolor=green];
	11 -> 12 [label="Spouse", dir=none, penwidth=2, color="blue"];
	12 [label="Sheila Flemmings\n1924 - 2015\nAge: 91\nClan: Silverwood\nGen:5", shape=rectangle, style=filled, fillcolor=green];
	11 -> 15[penwidth=2];
	15 [label="Charles Flemmings\n1947 - 2000\nAge: 53\nClan: Silverwood\nGen: 6", shape=rectangle, style=filled, fillcolor=green];
	15 -> 16 [label="Spouse", dir=none, penwidth=2, color="blue"];
	16 [label="Jane Flemmings\n1960 - 2021\nAge: 61\nClan: Silverwood\nGen:6", shape=rectangle, style=filled, fillcolor=green];
	15 -> 24[penwidth=2];
	24 [label="Emma Flemmings\n2000 - Still Alive\nAge: 23\nClan: Silverwood\nGen: 7", shape=rectangle, style=filled, fillcolor=green];
	11 -> 17[penwidth=2];
	17 [label="Daniella Flemmings\n1922 - Still Alive\nAge: 101\nClan: Blackthorn\nGen: 6", shape=rectangle, style=filled, fillcolor=orange];
	17 -> 18 [label="Spouse", dir=none, penwidth=2, color="blue"];
	18 [label="Joshua Richardson\n1952 - Still Alive\nAge: 71\nClan: Blackthorn\nGen:6", shape=rectangle, style=filled, fillcolor=orange];
	17 -> 20[penwidth=2];
	20 [label="Joseph Richardson\n1977 - Still Alive\nAge: 46\nClan: Blackthorn\nGen: 7", shape=rectangle, style=filled, fillcolor=orange];
	20 -> 21 [label="Spouse", dir=none, penwidth=2, color="blue"];
	21 [label="Elaine Richardson\n1977 - Still Alive\nAge: 46\nClan: Blackthorn\nGen:7", shape=rectangle, style=filled, fillcolor=orange];
	20 -> 22[penwidth=2];
	22 [label="Eric Richardson\n1999 - Still Alive\nAge: 24\nClan: Blackthorn\nGen: 8", shape=rectangle, style=filled, fillcolor=orange];
	22 -> 23 [label="Spouse", dir=none, penwidth=2, color="blue"];
	23 [label="Edith Richardson\n2000 - Still Alive\nAge: 23\nClan: Blackthorn\nGen:8", shape=rectangle, style=filled, fillcolor=orange];
	22 -> 25[penwidth=2];
	25 [label="Craig Richardson\n2022 - Still Alive\nAge: 1\nClan: Blackthorn\nGen: 9", shape=rectangle, style=filled, fillcolor=orange];
	9 -> 13[penwidth=2];
	13 [label="Pamela Flemmings\n1923 - 2020\nAge: 97\nClan: Thornfield\nGen: 5", shape=rectangle, style=filled, fillcolor=yellow];
	13 -> 14 [label="Spouse", dir=none, penwidth=2, color="blue"];
	14 [label="Clifford Johnson\n1910 - 2002\nAge: 92\nClan: Thornfield\nGen:5", shape=rectangle, style=filled, fillcolor=yellow];
	13 -> 19[penwidth=2];
	19 [label="Anita Johnson\n1950 - 1955\nAge: 5\nClan: Thornfield\nGen: 6", shape=rectangle, style=filled, fillcolor=yellow];
	13 -> 40[penwidth=2];
	40 [label="Martin Johnson\n1953 - 2003\nAge: 50\nClan: Thornfield\nGen: 6", shape=rectangle, style=filled, fillcolor=yellow];
	40 -> 41 [label="Spouse", dir=none, penwidth=2, color="blue"];
	41 [label="Meradith Johnson\n1957 - 2022\nAge: 65\nClan: Thornfield\nGen:6", shape=rectangle, style=filled, fillcolor=yellow];
	40 -> 42[penwidth=2];
	42 [label="Kalyb Johnson\n1977 - Still Alive\nAge: 46\nClan: Thornfield\nGen: 7", shape=rectangle, style=filled, fillcolor=yellow];
	42 -> 43 [label="Spouse", dir=none, penwidth=2, color="blue"];
	43 [label="Mariya Johnson\n1978 - Still Alive\nAge: 45\nClan: Thornfield\nGen:7", shape=rectangle, style=filled, fillcolor=yellow];
	42 -> 44[penwidth=2];
	44 [label="Jiriya Johnson\n1999 - Still Alive\nAge: 24\nClan: Thornfield\nGen: 8", shape=rectangle, style=filled, fillcolor=yellow];
	42 -> 45[penwidth=2];
	45 [label="Sara Johnson\n1999 - Still Alive\nAge: 24\nClan: Thornfield\nGen: 8", shape=rectangle, style=filled, fillcolor=yellow];
	42 -> 46[penwidth=2];
	46 [label="Whitney Johnson\n1999 - Still Alive\nAge: 24\nClan: Thornfield\nGen: 8", shape=rectangle, style=filled, fillcolor=yellow];
	0 -> 26[penwidth=2];
	26 [label="Jim Stallings\n1825 - 1891\nAge: 66\nClan: Oakenheart\nGen: 2", shape=rectangle, style=filled, fillcolor=purple];
	26 -> 33 [label="Spouse", dir=none, penwidth=2, color="blue"];
	33 [label="Amy Stallings\n1826 - 1893\nAge: 67\nClan: Oakenheart\nGen:2", shape=rectangle, style=filled, fillcolor=purple];
	26 -> 34[penwidth=2];
	34 [label="Greg Stallings\n1852 - 1921\nAge: 69\nClan: Oakenheart\nGen: 3", shape=rectangle, style=filled, fillcolor=purple];
	34 -> 35 [label="Spouse", dir=none, penwidth=2, color="blue"];
	35 [label="Landry Stallings\n1855 - 1945\nAge: 90\nClan: Oakenheart\nGen:3", shape=rectangle, style=filled, fillcolor=purple];
	34 -> 36[penwidth=2];
	36 [label="Matt Stallings\n1887 - 1967\nAge: 80\nClan: Oakenheart\nGen: 4", shape=rectangle, style=filled, fillcolor=purple];
	36 -> 37 [label="Spouse", dir=none, penwidth=2, color="blue"];
	37 [label="Maddison Stallings\n1887 - 1972\nAge: 85\nClan: Oakenheart\nGen:4", shape=rectangle, style=filled, fillcolor=purple];
	36 -> 39[penwidth=2];
	39 [label="Jimmy Stallings\n1923 - 1925\nAge: 2\nClan: Oakenheart\nGen: 5", shape=rectangle, style=filled, fillcolor=purple];
	34 -> 38[penwidth=2];
	38 [label="Leslie Stallings\n1887 - 1945\nAge: 58\nClan: Oakenheart\nGen: 4", shape=rectangle, style=filled, fillcolor=purple];
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
44,Jiriya,Johnson,F,1999,,,,42,43,Thornfield,8
45,Sara,Johnson,F,1999,,,,42,43,Thornfield,8
46,Whitney,Johnson,F,1999,,,,42,43,Thornfield,8
47,Peter,Harrison,M,1979,,44,,29,30,Brazenbush,7
48,Ezekiel,Harrison,M,1999,,23,,31,32,Brazenbush,8
49,Bartholomew,Harrison,M,2002,,,,31,32,Brazenbush,8
50,Charolette,Harrison,F,1997,,,51,31,32,Ironhammer,8
51,Jerimiah,Jefferies,M,1997,,,50,,,Ironhammer,8
52,Elizabeth,Jefferies,F,2023,,,,50,51,Ironhammer,9
```
