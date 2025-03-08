from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from tools.custom_tool import load_examples
from crewai_tools.tools import JSONSearchTool  # Updated import path

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Aitutor():
	"""Aitutor crew"""

	
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	# Create a JSON knowledge source
	# json_source = JSONKnowledgeSource(
	# 	file_paths=["training_set.json",], 
	# )
	
	# llm = LLM(
	# 	model="gemini/gemini-2.0-flash",
	# 	temperature=0.3,
	# 	api_key="AIzaSyBMLXoaoDU8gMe0qLNWGA91tOxx4GNfvew"
	# )

	llm = LLM(
		model="ollama/deepseek-v2:16b",
		temperature=0.3,
		base_url="http://localhost:11434"
	)

	# jsonSearchTool = JSONSearchTool(
	# 	json_path="training_set.json",
	# 	config={
	# 		"llm": {
	# 			"provider": "google",  # Other options include google, openai, anthropic, llama2, etc.
	# 			"config": {
	# 				"model": "gemini/gemini-2.0-flash",
	# 				"api_key": "AIzaSyBMLXoaoDU8gMe0qLNWGA91tOxx4GNfvew",
	# 				# Additional optional configurations can be specified here.
	# 				# temperature=0.5,
	# 				# top_p=1,
	# 				# stream=true,
	# 			},
	# 		},
	# 		"embedder": {
	# 			"provider": "google", # or openai, ollama, ...
	# 			"config": {
	# 				"model": "models/text-embedding-004",
	# 				"task_type": "retrieval_document",
	# 				# Further customization options can be added here.
	# 			},
	# 		},
    # 	},
	# )

	@agent
	def solver_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['solver_agent'],
			llm=self.llm,
			max_iter=40,
			memory=True,
		)
	
	# @agent
	# def search_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['search_agent'],
	# 		verbose=True,
	# 		llm=self.llm,
	# 	)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def solve_math(self) -> Task:
		return Task(
			config=self.tasks_config['solve_math'],
		)

	# @task
	# def search_explanation(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['search_explanation'],
	# 		tools=[self.jsonSearchTool],
	# 		async_execution=True,
	# 		output_file='sample_explanation.md'
	# 	)
	
	# @task
	# def explan_solution(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['explan_solution'],
	# 		context=[self.search_explanation(), self.solve_math()],
	# 		output_file='explanation.md'
	# 	)
	
	# @task
	# def evaluate_math_explanation(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['evaluate_math_explanation'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Aitutor crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
