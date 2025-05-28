from agents import Agent, handoff
from industry_finder import agent as industry_finder_agent
from car_rental_leasing import agent as car_rental_leasing_agent
from insurance import agent as insurance_agent


agent = Agent(
    name="ESG agent",
    instructions= open("Prompts/esg.md").read(),
    model="gpt-4o-mini",
    handoffs=[industry_finder_agent, car_rental_leasing_agent, insurance_agent]
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "What are the key sustainability disclosure topics and metrics for the Car Rental & Leasing industry?")
    print(result.final_output)