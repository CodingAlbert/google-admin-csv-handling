#!/usr/bin/env bash

# Function to print help
print_help() {
    echo "Usage: $0 -a <alias_assignment_csv> -s <sender_email>"
    echo
    echo "Arguments:"
    echo "  -a <alias_assignment_csv>  CSV file with headers 'user' and 'alias' containing the email aliases to be assigned."
    echo "  -s <sender_email>  The email address to send notifications from."
    echo
    echo "Example:"
    echo "  $0 -a alias_assignment.csv -s admin@example.com"
}

# Check if arguments are provided
if [ "$#" -eq 0 ]; then
    print_help
    exit 1
fi

# Parse arguments
while getopts "a:s:" opt; do
    case $opt in
        a)
            ALIAS_ASSIGNMENT_FILE="$OPTARG"
            ;;
        s)
            SENDER_EMAIL="$OPTARG"
            ;;
        *)
            print_help
            exit 1
            ;;
    esac
done

# Check if all required arguments are provided
if [ -z "$ALIAS_ASSIGNMENT_FILE" ] || [ -z "$SENDER_EMAIL" ]; then
    print_help
    exit 1
fi

# Email subject
EMAIL_SUBJECT="Google Workspace: Máš nový školní emailový alias!"

# Template for email body
EMAIL_BODY_TEMPLATE=$(cat <<'EOF'
Ahoj %USERNAME%,

Pro anonymní registraci do internetových služeb bez použití Google účtu jsem ti vytvořil 
alias email:  %ALIAS%

Při registraci do služby, která neumožňuje použití Google účtu použij jako 
emailovou adresu tento email.

S pozdravem,
IT Podpora ZŠ Livingston
EOF
)
# Function to send an email using GAM
send_email() {
    local recipient_email=$1
    local alias_email=$2
    local username=$(echo $recipient_email | cut -d '@' -f 1)
    local email_body=$(echo "$EMAIL_BODY_TEMPLATE" | sed "s/%USERNAME%/$username/g" | sed "s/%ALIAS%/$alias_email/g")

    gam sendemail "$recipient_email" subject "$EMAIL_SUBJECT" message "$email_body" from "$SENDER_EMAIL"
}

# Read the alias assignment file and process each entry
while IFS=, read -r user_email alias_email; do
    # Skip the header line
    if [ "$user_email" == "user" ]; then
        continue
    fi

    if [ -n "$user_email" ] && [ -n "$alias_email" ]; then
        # Add alias
        gam create alias "$alias_email" user "$user_email"
        if [ $? -eq 0 ]; then
            echo "Alias $alias_email added to user $user_email"
            
            # Send email notification
            send_email "$user_email" "$alias_email"
        else
            echo "Failed to add alias $alias_email to user $user_email"
        fi
    fi
done < "$ALIAS_ASSIGNMENT_FILE"

echo "Alias assignment completed. Output file: $ALIAS_ASSIGNMENT_FILE"
