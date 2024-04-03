# explainer.py
from dotenv import load_dotenv
from langchain_openai import OpenAI  # Updated import
load_dotenv()


langchain_explainer = OpenAI(api_key=os.getenv('OAKEY'))

def explain_code_changes(improvements):
    """
    Generate explanations for the given improvements.
    """
    explanations = []
    for improvement in improvements:
        # Craft a detailed prompt for each improvement to get its explanation
        prompt = f"Explain why this change improves accessibility: {improvement}"
        explanation = langchain_explainer(prompt)
        explanations.append(explanation)
    return explanations
