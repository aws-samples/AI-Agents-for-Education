# Bedrock Agents for EDU Use Cases

This repository showcases example Bedrock Agents created for educational use cases.

## Repo Structure

- **Data:** Sample data that connects to the agents.
- **Tools:** Tools for agents to use.
- **Production:** Web UI and Bedrock agent integration.

## Agent Example 1: Course Recommendation Agent

- **Name:** Course Recommendation Agent
- **Target Audience:** Higher-Ed Student Advisors
- **Sample questions:** how many credits student 1 has earned? What courses are offerred this semester (202408) that's relevant to this student's major? Does this course conflict with student's schedule? What course do you recommend for student 1 to take this semester (202408) 

### Deployment Instructions

1. **Prepare Data:** Run the `data-prep-course-recommendation-agent.ipynb` notebook to prepare the necessary data.
2. **Launch Agent:** Execute the `course-recommendation-agent.ipynb` notebook to deploy the agent in your AWS account.

### Architecture

![Course Recommendation Agent Architecture](image/course-recommendation-agent.png)

