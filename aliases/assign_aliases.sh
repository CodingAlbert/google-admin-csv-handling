#!/usr/bin/env bash

# Function to print help
print_help() {
    echo "Usage: $0 <alias_assignment_csv>"
    echo
    echo "Arguments:"
    echo "  <alias_assignment_csv>  CSV file with headers 'user' and 'alias' containing the email aliases to be assigned."
    echo
    echo "Example:"
    echo "  $0 alias_assignment.csv"
}

# Check if the alias assignment file is provided
if [ -z "$1" ]; then
    print_help
    exit 1
fi

# Define the alias assignment file
ALIAS_ASSIGNMENT_FILE="$1"

# Define the sender email address
SENDER_EMAIL="admin@example.com"

# Email subject
EMAIL_SUBJECT="New Email Alias Added"

# Template for email body
EMAIL_BODY_TEMPLATE=$(cat <<'EOF'
Hi %USERNAME%,

We have added a new email alias to your account: %ALIAS%

Best regards,
Your IT Team
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
        gam update user "$user_email" add alias "$alias_email"
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
