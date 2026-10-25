import re


def detect_sql_injection(user_input):
    suspicious_patterns = [
        r"\bOR\b\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?",
        r"--",
        r"\bUNION\b\s+\bSELECT\b",
        r";\s*(DROP|DELETE|UPDATE|INSERT)\b",
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True

    return False


def main():
    print("=== SQL INJECTION INPUT DETECTOR ===")

    user_input = input("Enter a sample input to analyze: ")

    if detect_sql_injection(user_input):
        print("\nWARNING: Suspicious SQL injection pattern detected!")
    else:
        print("\nNo suspicious pattern detected by these rules.")

    print("\nNote: This simple detector is for educational purposes.")
    print("It may miss attacks or flag legitimate input.")


if __name__ == "__main__":
    main()