# AUTOMATE HANDLING GOOGLE ADMIN CSV FILES

I wrote these 4 scripts to simplify handling csv data for Google Admin Console.

## Main Script

Main script *generate_upload_csv.py* accesses a *user_downloads* folder where you
move all your csv files exported from Google Admin Console GUI. 
The script parses the files, generates new passwords for all users,and prepares them
for upload based on a template *users.csv* or any other template you provide it.

##Other Scripts

Other scripts are used for quick double checking of the files. 

*export_import_fieldnames_difference.py* checks the differences between template and csv files
exported from Google Admin Console GUI.

*export_import_users_difference.py* checks the differences in users between the exported csv files
and your *users_to_upload.csv* in case you do any manual meddling with the upload ready csv file.

*generate_passwords.py* generates a number of passwords in case you need any aditional passwords
using the same password parameters as the main script.