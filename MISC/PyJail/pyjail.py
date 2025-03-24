import ast

BANNED_WORDS = ['import', 'exec', 'eval', 'os', 'subprocess', 'system']
BANNED_NODES = [ast.Import, ast.ImportFrom]

def is_safe(code):
    for word in BANNED_WORDS:
        if word in code:
            print(f"Debug: Banned word detected - {word}")
            return False
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if type(node) in BANNED_NODES:
                print(f"Debug: Banned node detected - {type(node).__name__}")
                return False
    except Exception as e:
        print(f"Debug: AST parsing error - {e}")
        return False
    return True

print("================================================================")
print("Welcome to PyJail!")
print("You can execute Python commands, but some things are restricted 'import', 'exec', 'eval', 'os', 'subprocess', 'system'")
print("Underscores are Allowed ! Good Luck :)")
print("================================================================")

while True:
    user_input = input("$")
    if not is_safe(user_input):
        print("Error: Hhhhhhhhhhhhhhhhhhhhhhhhhhhhh!")
    else:
        try:
            exec(user_input)
        except Exception as e:
            print(f"Error: {e}")
