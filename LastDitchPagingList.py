import os

# Library names
library_names = [
    "Bookmobile Center", "Andrew Bayne", "A.C. Free", "Avalon", "Baldwin",
    "Bethel Park", "Braddock", "Brentwood", "Bridgeville", "Clairton",
    "Edgewood", "Forest Hills", "Cooper-Siegel", "Sharpsburg", "CLP Main",
    "Beechview", "Brookline", "Carrick", "Downtown", "East Liberty",
    "Hazelwood", "Hill District", "Homewood", "Knoxville", "Lawrenceville",
    "LAMP", "CLP Main", "Mt. Washington", "Sheraden", "Squirrel Hill",
    "West End", "Woods Run", "Harrison", "Castle Shannon", "Coraopolis",
    "Crafton", "Dormont", "Green Tree", "Hampton", "Homestead",
    "Jefferson Hills", "McKeesport", "Duquesne", "White Oak", "Millvale",
    "Monroeville", "Moon", "Mt. Lebanon", "North Versailles", "Northern Tier",
    "Pine", "Northland", "Oakmont", "Penn Hills", "Pleasant Hills", "Plum",
    "Robinson", "Scott", "Sewickley", "Shaler", "South Fayette",
    "South Park", "Springdale", "F.O.R. Sto-Rox", "Swissvale",
    "Upper St. Clair", "Western Allegheny", "Whitehall", "Wilkinsburg", "Eastridge"
]

def display_libraries(library_names):
    """Display library names in three columns."""
    num_columns = 3
    per_column = len(library_names) // num_columns + (len(library_names) % num_columns > 0)
    for start in range(0, len(library_names), per_column):
        end = start + per_column
        for i in range(start, min(end, len(library_names))):
            print(f"{i+1:4}. {library_names[i]}")

def extract_paging_data(file_path, library_name):
    """Extract paging data for the specified library from the file."""
    print(f"Opening file: {file_path}")
    if not os.path.exists(file_path):
        print("File does not exist.")
        return
    
    paging_data = []
    capture = False
    start_capturing = False  # Flag to start capturing data at the next line after 'LOCATION:'
    with open(file_path, 'r') as file:
        for line in file:
            if "LOCATION: " + library_name in line:
                capture = True
                start_capturing = True  # Start capturing from the next line
                print(f"Found LOCATION for {library_name}. Preparing to capture...")
            elif capture and start_capturing:
                if line.startswith("10:"):
                    start_capturing = False  # Reset flag after finding the first '10:'
                    if paging_data:
                        yield paging_data
                        paging_data = []
                    print("Found new block start, yielding previous data.")
                paging_data.append(line.strip())

    if paging_data:
        yield paging_data

# Display libraries
display_libraries(library_names)

# User input
selected_index = int(input("Enter the number of the library you want: ")) - 1
selected_library = library_names[selected_index]
date_str = input("Enter the date in YYYY_MM_DD format: ")
file_path = f"//einetwork.net/shares/pagingslips/{date_str}.txt"

# Process data and write to file
with open("rescuePagingList.txt", "w") as outfile:
    for data_block in extract_paging_data(file_path, selected_library):
        outfile.write("-" * 20 + "\n")
        outfile.write("\n".join(data_block) + "\n")

print(f"Paging data for {selected_library} saved to 'rescuePagingList.txt'.")
