import os
from dotenv import load_dotenv
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationEntityMemory
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

class AccessibilityProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_html = None
        self.soup = None
        self.updated_html = None
        self.analysis_agent = None
        self.summary_agent = None
        self.api_key = os.getenv("OPENAI_API_KEY")
        OpenAI.api_key = self.api_key

    def initialize_agents(self):
        """Initialize the agents for analyzing and summarizing HTML."""
        self.analysis_agent = self.create_agent('./agent_prompts/wcag_compliance_agent.txt', "gpt-3.5-turbo")
        self.summary_agent = self.create_agent('./agent_prompts/update_summarizer_agent.txt', "gpt-3.5-turbo")

    def create_agent(self, agent_def_path, model_name):
        """Helper function to create an agent with a given prompt file and model."""
        with open(agent_def_path, 'r') as f:
            system_prompt_content = f.read()

        chat_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt_content),
            HumanMessagePromptTemplate.from_template("{user_input}")
        ])

        llm = ChatOpenAI(model_name=model_name, temperature=0, request_timeout=120)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        return LLMChain(llm=llm, prompt=chat_template, verbose=True, memory=memory)

    def load_and_parse_html(self):
        """Load HTML from file and parse it using BeautifulSoup."""
        with open(self.file_path, 'r') as file:
            self.original_html = file.read()
        self.soup = BeautifulSoup(self.original_html, 'html.parser')

    def analyze_html(self):
        """Use the analysis LLM to update HTML for accessibility."""
        formatted_input = {"user_input": str(self.soup)}
        response = self.analysis_agent.run(formatted_input)
        self.updated_html = response
        self.soup = BeautifulSoup(self.updated_html, 'html.parser')

    def summarize_changes(self):
        """Use the summary LLM to generate a summary of HTML changes."""
        user_input = f"Original HTML: {self.original_html}\nUpdated HTML: {self.updated_html}"
        formatted_input = {"user_input": user_input}
        summary_response = self.summary_agent.run(formatted_input)
        return summary_response

    def save_html(self, content, filename, directory="updated_html_files"):
        """Generalized function to save HTML content to a specified file."""
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"{filename} saved to {file_path}")

    def process(self):
        """Full process method to run the accessibility analysis and summarization."""
        self.load_and_parse_html()
        self.analyze_html()
        self.save_html(self.updated_html, "updated_page.html")  # Save the updated HTML
        changes_summary = self.summarize_changes()
        self.save_html(changes_summary, "changes_summary.html")  # Save the summary of changes as HTML
        print("Changes Summary:", changes_summary)

        # Add to the bottom of your existing AccessibilityProcessor class

    def process_html_file(file_path):
        processor = AccessibilityProcessor(file_path)
        processor.initialize_agents()
        processor.load_and_parse_html()
        processor.analyze_html()
        changes_summary = processor.summarize_changes()
        processor.save_html(processor.updated_html, "updated_page.html")
        return changes_summary, processor.updated_html


if __name__ == "__main__":
    file_path = '/Users/williammisiaszek/Code/AApp/back-end/venv/sample.html'
    processor = AccessibilityProcessor(file_path)
    processor.initialize_agents()
    processor.process()
