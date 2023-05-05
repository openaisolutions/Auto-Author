import yaml

def fix_yaml_titles(file_path):
    # Load the original YAML content
    with open(file_path, 'r') as infile:
        yaml_content = yaml.safe_load(infile)
    
    # Recursive function to fix titles in the YAML structure
    def fix_titles(obj):
        if isinstance(obj, list):
            for item in obj:
                fix_titles(item)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'title' and ':' in value:
                    # Wrap the title in quotes if it contains a colon
                    obj[key] = f'"{value}"'
                fix_titles(value)
    
    # Apply the fix to the loaded YAML content
    fix_titles(yaml_content)
    
    # Overwrite the original YAML file with the fixed content
    with open(file_path, 'w') as outfile:
        yaml.dump(yaml_content, outfile, default_flow_style=False, sort_keys=False)

# Specify the file path of the YAML file to be fixed
file_path = '_toc.yaml'

# Run the script to fix the YAML titles and overwrite the original file
fix_yaml_titles(file_path)
