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
    """
    Recursively finds all HTML files within the given directory.
    """
    html_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.endswith('.html') or file.endswith('.html.erb'):
                html_files.append(os.path.join(root, file))
    return html_files

def analyze_code(file_path):
    """
    Analyze the HTML file for accessibility issues and return the improved HTML.
    """
    with open(file_path, 'r') as file:
        html_content = file.read()

    # Craft a prompt for LangChain to suggest accessibility improvements
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

    # Use LangChain to invoke a request for suggestions
    response = langchain_analyzer.invoke(prompt)  # Make sure to use the invoke method

    # Here, we assume that the response is a string containing the improved HTML content
    # This is a placeholder; depending on the actual response format, parsing may be required
    improved_html_content = response

    # Return the improved HTML content
    return improved_html_content

def save_improved_html(html_file, improved_html_content):
    """
    Save the improved HTML content to a new file.

    Args:
    - html_file (str): The path to the original HTML file.
    - improved_html_content (AIMessage): The improved HTML content.

    Returns:
    - new_file_path (str): The path to the new file with improved HTML content.
    """
    try:
        # Extract the file name from the original path
        file_name = os.path.basename(html_file)
        # Construct the new file path
        new_file_path = os.path.join(os.path.dirname(html_file), "improved_" + file_name)
        
        # Print the improved HTML content for debugging
        print("Improved HTML content:")
        print(improved_html_content)
        
        # Open the new file in write mode
        with open(new_file_path, "w") as file:
            # Convert AIMessage object to string before writing
            file.write(str(improved_html_content))
        
        print(f"Improved HTML content saved to: {new_file_path}")
        return new_file_path
    except Exception as e:
        print(f"Error saving improved HTML content: {e}")
        return None


def perform_accessibility_improvement(start_path):
    """
    Entry function to find HTML files and perform accessibility improvements.
    """
    # Find all HTML files in the given directory path
    html_files = find_html_files(start_path)

    # Dictionary to store the mapping of original files to their improved versions
    improved_files = {}

    # Loop through each HTML file
    for html_file in html_files:
        # Analyze the HTML content for accessibility improvements
        improved_html_content = analyze_code(html_file)

        # Save the improved HTML content to a new file
        new_file_path = save_improved_html(html_file, improved_html_content)

        # Add the original and new file paths to the dictionary
        improved_files[html_file] = new_file_path

    # Return the dictionary containing the original and improved file paths
    return improved_files
