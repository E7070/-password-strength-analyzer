import re
import math

def check_length(password):
    return len(password)

def check_upper(password):
    return len(re.findall(r'[A-Z]', password))

def check_lower(password):
    return len(re.findall(r'[a-z]', password))

def check_digits(password):
    return len(re.findall(r'\d', password))

def check_symbols(password):
    return len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))

password = input("Enter password: ")
print(password)

def load_common_passwords():
    try:
        with open("commonpwd.txt", "r") as f:
            return set(p.strip() for p in f.readlines())
    except:
        return set()

def calculate_entropy(password):
    pool = 0
    if re.search(r'[a-z]', password): pool += 26
    if re.search(r'[A-Z]', password): pool += 26
    if re.search(r'\d', password): pool += 10
    if re.search(r'[^a-zA-Z0-9]', password): pool += 32

    if pool == 0:
        return 0

    return round(len(password) * math.log2(pool), 2)

def estimate_crack_time(entropy):
    guesses_per_sec = 1e9
    seconds = (2 ** entropy) / guesses_per_sec

    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"

def analyze(password):
    common = load_common_passwords()

    score = 0
    tips = []

    if check_length(password) >= 12: score += 2
    else: tips.append("Use at least 12 characters.")

    if check_upper(password): score += 1
    else: tips.append("Add uppercase letters.")

    if check_lower(password): score += 1
    else: tips.append("Add lowercase letters.")

    if check_digits(password): score += 1
    else: tips.append("Add numbers.")

    if check_symbols(password): score += 1
    else: tips.append("Add symbols.")

    if password.lower() in common:
        tips.append("Password is too common.")
        score = 0

    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    if score <= 2: strength = "Weak"
    elif score <= 4: strength = "Medium"
    elif score <= 6: strength = "Strong"
    else: strength = "Very Strong"

    return {
        "length": len(password),
        "entropy": entropy,
        "strength": strength,
        "crack_time": crack_time,
        "tips": tips
    }
