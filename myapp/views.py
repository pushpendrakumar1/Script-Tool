import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myapp.constants import variable_styles


@csrf_exempt  # For demonstration purposes, disable CSRF protection. Not recommended for production.
def replace_variables(request):
    variables_to_replace = [
        'FieldReplaceableUnit_value(RRU-7)',
        'AntennaUnitGroup_value',
        'Site_id',
        'dlAttenuation_value',
        'ulAttenuation_value',
        'dlTrafficDelay_value',
        'ulTrafficDelay_value',
        'RfBranch_3_value',
        'RfBranch_4_value',
        'RfBranch_8_value',
        'SectorCarrier_7_value',
        'SectorEquipmentFunction_7_value'
    ]

    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Extract the original file name
            original_file_name = uploaded_file.name

            # Save the uploaded file to a temporary location
            file_path = os.path.join(settings.MEDIA_ROOT, original_file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Prompt the user to enter values for the variables
            variable_values = {}
            for variable in variables_to_replace:
                value = request.POST.get(variable)
                variable_values[variable] = value

            # Replace variable names with their values in the input text
            with open(file_path, 'r') as input_file:
                input_text = input_file.read()
                for variable, value in variable_values.items():
                    input_text = input_text.replace(variable, value)

            # Generate the output file name with the same base name as the original file
            base_name, extension = os.path.splitext(original_file_name)
            output_file_name = f"{base_name}_output.txt"
            output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)

            with open(output_file_path, 'w') as output_file:
                output_file.write(input_text)

            # Provide a download link for the output file
            output_file_url = output_file_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)

            return render(request, 'replace_variables.html', {'output_file_url': output_file_url})

    return render(request, 'replace_variables.html', {'variables_to_replace': variables_to_replace})



# ----------------------------------------converter-------------------------------------------
import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from .your_script import process_and_convert_scripts
from django.shortcuts import render
import shutil

def process_view(request):
    output_files = []
    download_links = []  # Initialize download_links here

    if request.method == 'POST':
        input_folder1 = request.POST.get('input_folder1')
        input_folder2 = request.POST.get('input_folder2')
        enter_id1 = request.POST.get('enter_id1')
        enter_id2 = request.POST.get('enter_id2')

        output_files = process_and_convert_scripts(input_folder1, input_folder2, enter_id1, enter_id2)

        # Move the generated files to the "media" directory
        for output_file in output_files:
            # Construct the destination path in the "media" directory
            destination_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(output_file))

            # Check if the file already exists, and if so, remove it
            if os.path.exists(destination_path):
                os.remove(destination_path)

            # Move the file to the destination path, overwriting if it already exists
            shutil.move(output_file, destination_path)
            
        output_files = process_and_convert_scripts(input_folder1, input_folder2, enter_id1, enter_id2)

        # Move the generated files to the "media" directory
        for output_file in output_files:
            # Construct the destination path in the "media" directory
            destination_path = os.path.join(settings.MEDIA_ROOT, output_file)

            # Move the file to the destination path
            os.rename(output_file, destination_path)

            # Generate the download link for the file
            download_url = os.path.join(settings.MEDIA_URL, output_file)
            download_links.append(download_url)   
            
            

        # Generate the download links for the files after moving them
        download_links = [os.path.join(settings.MEDIA_URL, os.path.basename(file)) for file in output_files]

    return render(request, 'process.html', {'download_links': download_links})




def download_script(request, script_path):
    # Open the file in binary mode for reading
    with open(script_path, 'rb') as file:
        response = FileResponse(file)
        # Set the Content-Disposition header for attachment
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(script_path)}"'
        return response
    
    
