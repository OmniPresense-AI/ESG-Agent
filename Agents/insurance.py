from agents import Agent, FileSearchTool, Runner
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get vector store ID from environment variable
VECTOR_STORE_ID = os.getenv('VECTOR_STORE_ID')

agent = Agent(
    name="Insurance Agent",
    instructions= open("Prompts/insurance.md").read(),
    model="gpt-4o-mini",
    tools=[
        FileSearchTool(
            vector_store_ids=[VECTOR_STORE_ID],
        )
    ]
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "What are the key sustainability disclosure topics and metrics for the Car Rental & Leasing industry?")
    print(result.final_output)
