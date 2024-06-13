# Google Admin CSV Automation Scripts

This repository contains a collection of scripts designed to simplify the handling of CSV data for the Google Admin Console. The main script parses CSV files exported from the Google Admin Console, generates new passwords for all users, and prepares them for upload. Additional scripts are provided for double-checking the files, generating additional passwords.

A new series of scripts (Alias Scripts) provides tools for generating and managing email aliases using python and GAM. The aliases are based on combination of adj and animal nouns and are localised for English (master branch) and Czech (cs_email branch).

## Scripts

### Main Script - Google Admin Console GUI

- `generate_upload_csv.py`: This script parses CSV files exported from the Google Admin Console, generates new passwords for all users, and prepares them for upload. This method requires using Google Admin Console GUI.

### Additional Scripts

- `export_import_fieldnames_difference.py`: This script checks the differences between the template and CSV files exported from the Google Admin Console GUI.

- `export_import_users_difference.py`: This script checks the differences in users between the exported CSV files and your `users_to_upload.csv`.

- `generate_passwords.py`: This script generates a number of passwords in case you need any additional passwords.

### Usage

1. Move your exported CSV files from the Google Admin Console to the `user_downloads` folder.
2. Run the `generate_upload_csv.py` script.
3. (Optional) Run the `export_import_fieldnames_difference.py` and `export_import_users_difference.py` scripts to check for differences.
4. (Optional) Run the `generate_passwords.py` script if you need to generate additional passwords.

### Alias Scripts - GAM

- `generate_aliases_csv.py`: This script generates a CSV file with a specified number of unique aliases.

- `combine_aliases.sh`: This script combines a CSV file of users with a file of aliases, assigning each user a unique alias.

- `assign_aliases.sh`: This script assigns each user an alias from the combined CSV file and sends an email notification to the user.

### Usage

1. Run the `generate_aliases_csv.py` to generate a list of adj, animal noun aliases. The script is available for Czech aliases and for English aliases. Even though the script has a vulgarity check, read the aliases to avoid undesirable combinations.
2. Run `combine_aliases.sh` to pair generated aliases with users.
3. Run `assign_aliases.sh` scripts to assign email aliases to users and notify the users via email. To customize the email, just edit the script.

#### GAM (Google Admin SDK)

These scripts use the [GAMADV-XTD3](https://github.com/taers232c/GAMADV-XTD3) fork of GAM (Google Apps Manager), a command line tool for Google Workspace Administrators. GAMADV-XTD3 extends the capabilities of GAM, adding many new features and capabilities. You'll need to have GAMADV-XTD3 installed and configured for these scripts to work.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.