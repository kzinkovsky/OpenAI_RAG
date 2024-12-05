def safe_float_input(prompt, default):
    """
    Prompts the user to enter a float value and returns it as the result.
    Args:
        prompt: a hint for the user with a brief explanation what to enter,
        default: the default value that is returned if the user enters it incorrectly
    Returns:
        a floating point value entered by the user or a default value 
    """
    while True:
        try:
            value = input(prompt).strip()
            return float(value) if value else default
        except ValueError:
            print(f"Invalid input. Please enter a number (integer or decimal) or leave blank for default ({default}).")

def safe_int_input(prompt, default):
    """
    Prompts the user to enter an integer value and returns it as the result.
    Args:
        prompt: a hint for the user with a brief explanation what to enter,
        default: the default value that is returned if the user enters it incorrectly
    Returns:
        an integer value entered by the user or a default value 
    """
    while True:
        try:
            value = input(prompt).strip()
            return int(value) if value else default
        except ValueError:
            print(f"Invalid input. Please enter a number (integer or decimal) or leave blank for default ({default}).")