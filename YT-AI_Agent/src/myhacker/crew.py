from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool
from myhacker.tools.requester import HttpRequesterTool
from myhacker.tools.jwt_manipulater import JwtManipulationTool
import litellm
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

# Configure litellm
os.environ["OPENAI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
litellm.api_key = os.getenv("GOOGLE_API_KEY")
"""
llm=ChatGoogleGenerativeAI(
	model="gemini-1.5-flash",
	verbose=True, 
	temperature=0.5,
	google_api_key=os.getenv("GOOGLE_API_KEY"))
"""
llm = ChatOpenAI(
    model_name="gemini/gemini-1.5-flash",  
    temperature=0.5,
    openai_api_key=os.getenv("GOOGLE_API_KEY"),
    max_tokens=1000
)


@CrewBase
class MyHackerCrew():
	"""MyHacker crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def myhacker(self) -> Agent:
		return Agent(
			config=self.agents_config['myhacker'],
			tools=[FileReadTool(), FileWriterTool(), DirectoryReadTool(),HttpRequesterTool(), JwtManipulationTool()],
			verbose=True,
			llm=llm
		)
	
	@task
	def create_jwt_none_attack_vector_task(self) -> Task:
		return Task(
			config=self.tasks_config['create_jwt_none_attack_vector_task'],
			tools=[FileReadTool(), FileWriterTool(), DirectoryReadTool(), JwtManipulationTool()],
			chunk_size=512,  # Process data in smaller chunks
			output_file='outputs/create_jwt_none_attack_vector_task.txt',
			create_directory=True
		)
	
	@task
	def execute_jwt_none_attack_vector_task(self) -> Task:
		return Task(
			config=self.tasks_config['execute_jwt_none_attack_vector_task'],
			tools=[FileReadTool(), FileWriterTool(), DirectoryReadTool(), HttpRequesterTool()],
			chunk_size=512,  # Process data in smaller chunks
			output_file='outputs/execute_jwt_none_attack_vector_task.txt',
    		create_directory=True,
			context=[self.create_jwt_none_attack_vector_task()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Myhacker crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			output_log_file="myhacker.log"
		)