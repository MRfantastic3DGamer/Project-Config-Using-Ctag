import subprocess
import json
import os

def generate_tags_file(project_path, tags_file_path):
    """Generate tags file using the ctags command."""
    try:
        # Run the ctags command
        subprocess.run(['ctags', '-R', '-f', tags_file_path, project_path], check=True)
        print(f"Tags file generated: {tags_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating tags file: {e}")
        exit(1)

def parse_tags_file(tags_file_path):
    """Parse the generated tags file and return a list of tags."""
    tags = []

    if not os.path.exists(tags_file_path):
        print(f"Tags file not found: {tags_file_path}")
        return tags

    with open(tags_file_path, 'r') as file:
        for line in file:
            # Ignore comment lines (starting with !)
            if line.startswith('!'):
                continue

            # Split the tag line by tab characters
            parts = line.split('\t')
            if len(parts) >= 4:
                tag_name = parts[0]
                file_name = parts[1]
                ex_command = parts[2]
                tag_field = parts[3].strip()

                # Create a dictionary for the current tag
                tag_info = {
                    "tag_name": tag_name,
                    "file_name": file_name,
                    "ex_command": ex_command,
                    "tag_field": tag_field
                }
                tags.append(tag_info)

    return tags

def write_json_file(data, output_file_path):
    """Write the parsed tag data to a JSON file."""
    with open(output_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    # Path to the project you want to generate tags for
    project_path = 'path_to_project'

    # Path to the tags file to be generated
    tags_file = 'tags_file'

    # Output path for the JSON file
    json_output_file = 'tags_output.json'

    # Generate the tags file using ctags
    generate_tags_file(project_path, tags_file)

    # Parse the tags file and generate a list of tags
    tags_data = parse_tags_file(tags_file)

    # Write the JSON file
    write_json_file(tags_data, json_output_file)

    print(f"JSON file has been created: {json_output_file}")