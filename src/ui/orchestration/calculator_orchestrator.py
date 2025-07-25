import os
import sys
import dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Load environment variables
dotenv.load_dotenv()

from ui.agents.business_analyst_agent import analyze_requirements
from ui.agents.software_engineer_agent import generate_plan_and_code
from ui.agents.product_owner_agent import review_solution

# Dasic Environment Check
required_keys = [
    "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_API_MODEL"
]

for key in required_keys:
    if not os.getenv(key):
        raise EnvironmentError(f"Missing required env variable: {key}")
    
# Simulated User Request
user_prompt = "Build a calculator app"

# Business Analyst
ba_output = analyze_requirements(user_prompt)
print("[Business Analyst Output]")
print(ba_output)

# Software Engineer
se_plan, se_code = generate_plan_and_code(ba_output)
print("\n[Software Engineer Plan]")
print(se_plan)
print("[Software Engineer Code]")
print(se_code)

# Product Owner
po_result = review_solution(se_plan, se_code)
print("\n[Product Owner Decision]")
print(po_result)

# Decision
if po_result.get("approved", False):
    print("\n Calculator app approved.")
else:
    print("\n Calculator app not approved.")