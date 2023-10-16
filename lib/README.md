# Configure your credentials
Rename the .env_sample file to .env
Update the values of the variables:
- your email to log in
- the event which is usually in the URL: e.g. https://saastock.brella.io/events/{EVENT}

## Get your session cookie
![Instructions for Brella](../static/brella_instructions.png)

# Run the script
```bash
python3 ./lib/brella.py
```