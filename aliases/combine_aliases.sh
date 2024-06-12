#!/usr/bin/env bash

# Function to print help
print_help() {
    echo "Usage: $0 -u <user_csv> -a <alias_file> -o <output_file>"
    echo
    echo "Arguments:"
    echo "  -u <user_csv>    CSV file with a header 'primaryEmail'"
    echo "  -a <alias_file>  Text file with one alias per line"
    echo "  -o <output_file> Output CSV file for user-alias pairs"
    echo
    echo "Example:"
    echo "  $0 -u ou_users.csv -a aliases.txt -o alias_assignment.csv"
}

# Check if arguments are provided
if [ "$#" -eq 0 ]; then
    print_help
    exit 1
fi

# Parse arguments
while getopts "u:a:o:" opt; do
    case $opt in
        u)
            USER_CSV="$OPTARG"
            ;;
        a)
            ALIAS_FILE="$OPTARG"
            ;;
        o)
            OUTPUT_FILE="$OPTARG"
            ;;
        *)
            print_help
            exit 1
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$USER_CSV" ] || [ -z "$ALIAS_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    print_help
    exit 1
fi

# Check if output file exists and create headers if it doesn't
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "user,alias" > "$OUTPUT_FILE"
fi

# Read the used aliases into an array
declare -A used_aliases
while IFS=, read -r user alias; do
    used_aliases["$alias"]=1
done < <(tail -n +2 "$OUTPUT_FILE")

# Read users into an array
declare -a users
while IFS=, read -r primaryEmail || [ -n "$primaryEmail" ]; do
    primaryEmail=$(echo "$primaryEmail" | tr -d '\r' | tr -d '\n') # Ensure no newlines or carriage returns
    users+=("$primaryEmail")
done < <(tail -n +2 "$USER_CSV")

# Debug: Print the users array
echo "Users read from CSV:"
for user in "${users[@]}"; do
    echo "User: '$user'"
done

# Read aliases into an array and filter out already used ones
declare -a aliases
while IFS= read -r alias; do
    alias=$(echo "$alias" | tr -d '\r' | tr -d '\n') # Ensure no newlines or carriage returns
    if [[ -z "${used_aliases[$alias]}" ]]; then
        aliases+=("$alias")
    fi
done < "$ALIAS_FILE"

# Debug: Print the aliases array
echo "Aliases available:"
for alias in "${aliases[@]}"; do
    echo "Alias: '$alias'"
done

# Assign aliases to users
for primaryEmail in "${users[@]}"; do
    # Debug: Print the current user being processed
    echo "Processing user: '$primaryEmail'"

    # Skip if primaryEmail is empty
    if [ -z "$primaryEmail" ]; then
        echo "Skipping empty primaryEmail"
        continue
    fi

    alias=${aliases[0]}
    if [ -z "$alias" ]; then
        echo "No more aliases available for $primaryEmail"
        break
    fi

    # Remove the first element from the array
    aliases=("${aliases[@]:1}")

    # Extract the domain from the primary email
    domain=$(echo "$primaryEmail" | awk -F@ '{print $2}')

    # Append the domain to the alias
    alias_with_domain="${alias}@${domain}"

    # Debug: Print the user and alias being written to the output file
    echo "Writing: '$primaryEmail','$alias_with_domain'"

    # Write the primaryEmail and alias_with_domain to the output file
    echo "$primaryEmail,$alias_with_domain" >> "$OUTPUT_FILE"
done

echo "Alias assignment completed. Output file: $OUTPUT_FILE"
