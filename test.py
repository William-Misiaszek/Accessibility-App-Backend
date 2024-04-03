# test.py
from analyzer import perform_accessibility_improvement

# Path to the directory containing the HTML file
directory_path = '/Users/williammisiaszek/Code/AApp/back-end/venv/'

# Run the analysis
improved_files = perform_accessibility_improvement(directory_path)

# Output the result
for original, improved in improved_files.items():
    print(f'Original file: {original}')
    print(f'Improved file: {improved}')
