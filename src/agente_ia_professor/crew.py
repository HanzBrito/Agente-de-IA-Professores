from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class AgenteIaProfessor():
    """AgenteIaProfessor crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    #===========================
    #Agente de IA Professor
    #===========================
    @agent
    def agente_professor_portugues(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_professor_portugues'], # type: ignore[index]
            verbose=True
        )
    #===========================
     #Agente de IA Matematica
    #===========================
    
    @agent

    def agente_professor_matematica(self) -> Agent:
            return Agent(
                config=self.agents_config['agente_professor_matematica'], # type: ignore[index]
                verbose=True
            )

    #===========================
     #Agente de IA Ciência
    #===========================
    @agent
    
    def agente_professor_ciencia(self) -> Agent:
                return Agent(
                    config=self.agents_config['agente_professor_ciencia'], # type: ignore[index]
                    verbose=True
                )
    #===========================
    #Agente de IA Reporta
    #===========================
    @agent
    def report_analistat(self) -> Agent:
        return Agent(
            config=self.agents_config['report_analista'], # type: ignore[index]
            verbose=True
        )

    @task
    def terefa_professor_portugues(self) -> Task:
        return Task(
            config=self.tasks_config['terefa_professor_portugues'], # type: ignore[index]
        )
    @task
    def terefa_professor_matematica(self) -> Task:
            return Task(
                config=self.tasks_config['terefa_professor_matematica'], # type: ignore[index]
            )
    @task
    def terefa_professor_ciencia(self) -> Task:
                return Task(
                    config=self.tasks_config['terefa_professor_ciencia'], # type: ignore[index]
                )

    @task
    def tarefa_reportada(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_reportada'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgenteIaProfessor crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
