# Bedrock Agents for EDU Use Cases

This repository showcases example Bedrock Agents created for educational use cases.

## Repo Structure

- **Data:** Sample data that connects to the agents.
- **Tools:** Tools for agents to use.
- **Production:** Web UI and Bedrock agent integration.

## Agent Example 1: Course Recommendation Agent

- **Name:** Course Recommendation Agent
- **Target Audience:** Higher-Ed Student Advisors
- **Sample questions:**
  - how many credits student 1 has earned?
  - What courses are offerred this semester (202408) that's relevant to this student's major?
  - Does the course "BIOL P110" conflict with student's schedule?
  - What course do you recommend for student 1 to take this semester (202408) 

### Architecture

![Course Recommendation Agent Architecture](image/course-recommendation-agent.png)

### Deployment Instructions of Course Recommendation Agent

1. **Prepare Data:** 

1.1 ***Structured data:*** Run the `data-prep-course-recommendation-agent-short.ipynb` notebook `Structured data preparation` section to prepare the tables.

1.2 ***Unstructured data:*** Run the `data-prep-course-recommendation-agent-short.ipynb` notebook `Unstructured data preparation` section to set up knowledge base.

2. **Launch Agent:** Run `course-recommendation-agent.ipynb` notebook to deploy the agent in your AWS account.

3. **Test Agent:** Use the above sample questions to test agent.

## Agent Example 2: Visual Math Agent
- **Description:** Agent creating math questions with visual artifacts
- **Target Audience:** Math curriculum designer, Math content creator, instructors
- **Sample questions:** create a multiple-choice question testing 3rd grader's understanding of equivalent fraction. create a question asking the time of an analog clock.

### Deployment Instructions of Visual Math Agent

**Launch Agent:** Run `visual-math-agent.ipynb` notebook to deploy the agent in your AWS account. 

## Agent Example 3: Course Assistant Agent (Coming soon)
- **Description:** Agent navigating course content to answer questions and making study plans.
- **Target Audience:** Students

## Agent Example 4: Multi-agent system for course recommendation
This is a multi-agent collaboration architecture for Agent Example 1
### Architecture

![Course Recommendation Agent Architecture](image/course-recommendation-multi-agent.png)
