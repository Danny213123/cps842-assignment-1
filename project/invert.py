from PathLib import Path

def process_cacm(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Example processing: Count number of lines and words
    lines = content.splitlines()
    num_lines = len(lines)
    num_words = len(content.split())
    
    print(f"File: {file_path}")
    print(f"Number of lines: {num_lines}")
    print(f"Number of words: {num_words}")