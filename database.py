import yaml
import os

# Data files of winners and everything else
WINNERS_DATA_YAML = "./data/winners.yaml"
ALL_POSTS_YAML = "./data/all.yaml"

def addEntriesToYaml(outfile, data):
    """
    Add the entries to the YAML file.
    If the file already exists, the new data is appended without duplicating entries.
    """
    if not isinstance(data, list):
        raise ValueError("Data should be a list of entries.")

    existing_data = []
    
    # Check if the file exists and read its content if it does
    if os.path.exists(outfile):
        with open(outfile, "r", encoding='utf-8') as f:
            existing_data = yaml.safe_load(f) or []

    # Ensure existing data is a list
    if not isinstance(existing_data, list):
        raise ValueError("Existing data in YAML file is not a list.")

    # Convert new data entries to their string representations
    data = [repr(item) for item in data]

    # Merge the existing data with the new data, avoiding duplication
    merged_data = existing_data + [item for item in data if item not in existing_data]

    # Write the combined data back to the file
    with open(outfile, "w", encoding='utf-8') as f:
        yaml.dump(merged_data, f, allow_unicode=True, default_flow_style=False)

def createDataDir():
    """
    Create the data directory if it does not exist.
    """
    absPath = os.path.abspath("./data")
    if not os.path.exists("./data"):
        os.makedirs("./data")
        print("Created data directory at full path: " + absPath)
    else:
        print("Data directory already exists at full path: " + absPath)

def listToYaml(list):
    """
    Convert a JSON string to a YAML string.
    """
    
    # Convert the Python object to a YAML string
    yaml_str = yaml.dump(list)
    
    return yaml_str

def addToWinners(responseList):
    """
    Add the winners to the winners.yaml file.
    """
    
    # Add the YAML entries to the winners.yaml file
    addEntriesToYaml(WINNERS_DATA_YAML, responseList)

def addToAllPosts(responseList):
    """
    Add the posts to the all.yaml file.
    """
    
    # Add the YAML entries to the all.yaml file1
    addEntriesToYaml(ALL_POSTS_YAML, responseList)

def countYamlEntries(yaml_file):
    """
    Count the number of entries in a YAML file.
    """
    if os.path.exists(yaml_file):
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f) or {}
            return len(data)
    else:
        return 0

def countRecordedWinners():
    """
    Count the number of recorded winners in the winners.yaml file.
    """
    return countYamlEntries(WINNERS_DATA_YAML)

def countRecordedPosts():
    """
    Count the number of recorded posts in the all.yaml file.
    """
    return countYamlEntries(ALL_POSTS_YAML)