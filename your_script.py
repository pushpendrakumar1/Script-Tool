import os
import re

def process_and_convert_scripts(input_folder1, input_folder2, enter_id1, enter_id2):
    try:
        # Create output folders with the same names as input folders
        output_folder1 = f"{input_folder1}_output"
        output_folder2 = f"{input_folder2}_output"
        os.makedirs(output_folder1, exist_ok=True)
        os.makedirs(output_folder2, exist_ok=True)

        def process_script(input_filename, output_filename, enter_id):
            try:
                
                # Open the input file for reading
                with open(input_filename, 'r') as input_file:
                    input_script = input_file.read()

                # Define the regex pattern to match "set," "set1x," and "lset1x" commands
                set_pattern = r'(\b(set|set1x|seti|lset1x))\s+(.*?)(?=\n|$)'
                converted_script = re.sub(set_pattern, rf'cmedit set SubNetwork=ONRM_ROOT_MO,MeContext={enter_id},ManagedElement={enter_id},\3', input_script)

                # Define the regex pattern to match "crn" commands
                crn_pattern = r'\bcrn\b'
                converted_script = re.sub(crn_pattern, rf'cmedit create SubNetwork=ONRM_ROOT_MO,MeContext={enter_id},ManagedElement={enter_id},', converted_script)
                converted_script = converted_script.replace('$', '')

                lines_to_remove = ['lt all', 'confb+', 'gs+', 'date = `date +%Y%m%d_%H%M%S`', 'confb-', 'commit', 'l-', 'l+']
                for line_to_remove in lines_to_remove:
                    converted_script = re.sub(re.escape(line_to_remove) + r'.*?$\n?', '', converted_script, flags=re.MULTILINE)

                # Modify each line in the script
                modified_script = []
                for line in converted_script.split('\n'):
                    # Remove '//' at the beginning of lines
                    modified_line = line.lstrip('//')
                    parts = modified_line.split()  # Split the modified line into words

                    if len(parts) > 3:
                        command = ' '.join(parts[:-2])  # Join all parts except the last two
                        value = parts[-2]
                        value = value.rstrip(':')  # Remove trailing colon if present

                        modified_line = f"{command} {value}:{parts[-1]}"

                    modified_script.append(modified_line)

                # Open the output file for writing
                with open(output_filename, 'w') as output_file:
                    output_file.write('\n'.join(modified_script))

                print(f"Processing completed. Modified script saved to {output_filename}")

            except FileNotFoundError:
                print(f"File not found: {input_filename}")

        # Loop through all files in the first input folder
        for filename in os.listdir(input_folder1):
            if filename.endswith('.mos'):
                input_path = os.path.join(input_folder1, filename)
                output_path = os.path.join(output_folder1, filename)
                process_script(input_path, output_path, enter_id1)

        # Loop through all files in the second input folder
        for filename in os.listdir(input_folder2):
            if filename.endswith('.mos'):
                input_path = os.path.join(input_folder2, filename)
                output_path = os.path.join(output_folder2, filename)
                process_script(input_path, output_path, enter_id2)

    except FileNotFoundError:
        print("One or more folders not found.")
        
    output_files = []

    # Loop through all files in the first input folder
    for filename in os.listdir(input_folder1):
        if filename.endswith('.mos'):
            input_path = os.path.join(input_folder1, filename)
            output_path = os.path.join(output_folder1, filename)
            process_script(input_path, output_path, enter_id1)
            output_files.append(output_path)

    # Loop through all files in the second input folder
    for filename in os.listdir(input_folder2):
        if filename.endswith('.mos'):
            input_path = os.path.join(input_folder2, filename)
            output_path = os.path.join(output_folder2, filename)
            process_script(input_path, output_path, enter_id2)
            output_files.append(output_path)

    return output_files
    
