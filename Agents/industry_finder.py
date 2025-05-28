from agents import Agent, ModelSettings, function_tool, FileSearchTool, Runner
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get vector store ID from environment variable
VECTOR_STORE_ID = os.getenv('VECTOR_STORE_ID')

agent = Agent(
    name="Industry Finder Agent",
    instructions= open("Prompts/industry_finder.md").read(),
    model="gpt-4o-mini",
    tools=[
        FileSearchTool(
            vector_store_ids=[VECTOR_STORE_ID],
        )
    ]
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "What is the SASB industry classification for a company that manufactures electric vehicles and renewable energy storage systems?")
    print(result.final_output)
