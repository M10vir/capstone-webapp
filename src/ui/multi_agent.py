import os
import re
import asyncio
import subprocess

from dotenv import load_dotenv

# Load .env from repo root, even if script is in subfolder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel

responses = []

def get_kernel():
    """Centralized Azure ChatCompletion kernel builder."""
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    service = AzureChatCompletion(
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    # Create and register Kernel
    kernel = Kernel()
    kernel.add_service(service)
    return kernel

class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""
    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate, if user's latest message contains 'APPROVED'."""
        for message in reversed(history.messages):
            if message.role == AuthorRole.USER and "APPROVED" in message.content.upper():
                return True
        return False 
    
def extract_html_from_chat(messages):
    """Extract HTML code block from SoftwareEngineer messages.""" 
    for message in reversed(messages):
        if message.role == AuthorRole.ASSISTANT and message.author_name == "SoftwareEngineer":
            match = re.search(r"```html\s*(.*?)```", message.content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
    return None

def save_html_to_file(html_code, filename="index.html"):
    """Save extracted HTML to file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"HTML code saved to {filename}") 

def trigger_git_push(script_path="push_to_github.sh"):
    """Trigger the Git push script via subprocess."""
    try:
        subprocess.run(["bash", script_path], check=True)
        print("Git push triggered via push_to_github.sh")
    except subprocess.CalledProcessError as e:
        print(f"Git push failed: {e}")

async def run_multi_agent(input: str):
    kernel = get_kernel()

    # Agent 1: Business Analyst
    business_analyst = ChatCompletionAgent(
        kernel=kernel,
        name="BusinessAnalyst",
        instructions="""You are a Business Analyst which will take the requirements from the user (also known as a 'customer') and create a project plan for creating the requested app. The Business Analyst understands the user requirements and creates detailed documents with requirements and costing. The documents should be usable by the SoftwareEngineer as a reference for implementing the required features, and by the Product Owner for reference to determine if the application delivered by the Software Engineer meets all of the user's requirements.""".strip()
    )

    # Agent 2: Software Engineer
    software_engineer = ChatCompletionAgent(
        kernel=kernel,
        name="SoftwareEngineer",
        instructions="""You are a Software Engineer, and your goal is create a web app using HTML and JavaScript by taking into consideration all the requirements given by the Business Analyst. The application should implement all the requested features. Deliver the code to the Product Owner for review when completed. You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.""".strip()
    )

    # Agent 3: Product Owner
    product_owner = ChatCompletionAgent(
        kernel=kernel,
        name="ProductOwner",
        instructions="""You are the Product Owner which will review the software engineer's code to ensure all user  requirements are completed. You are the guardian of quality, ensuring the final product meets all specifications. IMPORTANT: Verify that the Software Engineer has shared the HTML code using the format ```html [code] ```. This format is required for the code to be saved and pushed to GitHub. Once all client requirements are completed and the code is properly formatted, reply with 'READY FOR USER APPROVAL'. If there are missing features or formatting issues, you will need to send a request back to the SoftwareEngineer or BusinessAnalyst with details of the defect.""".strip()
    )

    # Prepare the AgentGroupChat
    agent_group = AgentGroupChat(
        agents=[business_analyst, software_engineer, product_owner]
    )

    # Add user message to history
    await agent_group.add_chat_message(
        ChatMessageContent(role=AuthorRole.USER, content=input)
    )

    async for content in agent_group.invoke():
        print(f"# {content.role}: '{content.content}'")
        responses.append(content)

    # Post-processing hook if APPROVED was detected
    for message in reversed(responses):
        if message.role == AuthorRole.USER and "APPROVED" in message.content.upper():
            print("Approval detected. Triggering finalization...")
            try:
                html_code = extract_html_from_chat(responses)
                if html_code:
                    save_html_to_file(html_code)
                    trigger_git_push()
                else:
                    print("No properly formatted HTML code found from SoftwareEngineer.")
            except Exception as e:
                print(f"Finalization error: {e}")
            break

    return responses

if __name__ == "__main__":
    import sys
    import asyncio

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    test_input = "Create a web calculator that support basic operation (+, -, *, /) with a terminal-based UI."
    asyncio.run(run_multi_agent(test_input))
