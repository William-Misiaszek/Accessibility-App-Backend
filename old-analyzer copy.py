import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # This is correct for using LangChain with OpenAI

# Load environment variables
load_dotenv()

# Ensure API key is present
api_key = os.getenv('OAKEY')
if not api_key:
    raise EnvironmentError("OAKEY environment variable is not set.")
else:
    print("OpenAI API key loaded successfully.")  # Debugging statement

# Initialize LangChain analyzer with explicit model specification
model_version = "gpt-4-turbo-preview"  # Specify the model you intend to use
langchain_analyzer = ChatOpenAI(api_key=api_key, model=model_version)
print(f"Initialized LangChain analyzer with model version: {model_version}")  # Debugging statement

def find_html_files(start_path):
    html_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.endswith('.html') or file.endswith('.html.erb'):
                html_files.append(os.path.join(root, file))
                print(f"Found HTML file: {os.path.join(root, file)}")  # Debugging statement
    if not html_files:
        print("No HTML files found in the specified directory.")  # Debugging statement
    return html_files

def analyze_code(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
        print(f"Reading file: {file_path}")  # Debugging statement

    prompt = (
    "First, evaluate the HTML content provided against the Web Content Accessibility Guidelines (WCAG) 2.1 AA standards. "
    "If the content already meets these standards, explain why it is compliant. If it does not, "
    "please suggest specific improvements to enhance its accessibility. The improvements should include: "
    "1. Adding descriptive alt attributes to all img tags for better screen reader compatibility. "
    "2. Ensuring headers are structured in a logical hierarchy to aid navigation for assistive technologies. "
    "3. Modifying color contrasts to be sufficient for users with visual impairments, following WCAG 2.1 AA contrast ratios. "
    "4. Implementing keyboard accessibility for all interactive elements, ensuring full navigability via keyboard alone. "
    "Include comments within the HTML to explain the improvements made or the reasons for compliance. "
    "Here is the HTML content:\n\n" + html_content
)

    print("Sending code for analysis...")  # Debugging statement
    response = langchain_analyzer.invoke(input=prompt)
    
    if 'choices' in response and response['choices']:
        improved_html_content = response['choices'][0]['text']
        print("Received improvement suggestions.")  # Debugging statement
    else:
        improved_html_content = "No improvements were suggested by the AI."
        print("No improvements were suggested by the AI.")  # Debugging statement

    return improved_html_content


def save_improved_html(original_file_path, improved_html_content):
    new_file_path = f"{original_file_path}.improved"
    with open(new_file_path, 'w') as file:
        file.write(improved_html_content)
        print(f"Saved improved HTML to: {new_file_path}")  # Debugging statement
    return new_file_path

def perform_accessibility_improvement(start_path):
    html_files = find_html_files(start_path)
    if not html_files:
        print("No HTML files found.")
        return {}

    # Debugging: print the number of HTML files found
    print(f"Total HTML files found: {len(html_files)}")

    results = {}
    for html_file in html_files:
        improved_html_content = analyze_code(html_file)
        if improved_html_content:  # Ensure there is content to save
            new_file_path = save_improved_html(html_file, improved_html_content)
            results[html_file] = new_file_path
        else:
            print(f"No improvements for {html_file}.")  # Debugging statement

    return results
