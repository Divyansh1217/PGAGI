��#   P G A G I 
 
 # Hiring Assistant Chatbot

## Project Overview
The Hiring Assistant Chatbot is a streamlined application designed to assist in the interview process by generating interview questions based on a given tech stack and evaluating candidate responses. It uses natural language processing (NLP) techniques powered by Hugging Face's transformers and Langchain for effective question generation and answer evaluation. The system is built on a modular architecture where you can customize the tech stack and evaluation criteria to suit various interview scenarios.

### Key Features:
- **Interview Question Generation**: Automatically generates relevant and diverse interview questions based on the tech stack.
- **Answer Evaluation**: Evaluates the candidate’s responses based on correctness and relevance using NLP models.
- **Tech Stack Customization**: Users can input a variety of programming languages, frameworks, and tools to get tailored interview questions.
- **Scoring System**: Assigns scores to the candidate’s answers on a scale from 0 to 10 based on relevance and correctness.

## Installation Instructions

To set up and run the Hiring Assistant Chatbot locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd hiring-assistant-chatbot
    ```

2. **Create a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate  # For Windows
    ```

3. **Install Dependencies**:
    Install the required Python libraries using pip.
    ```bash
    pip install -r requirements.txt
    ```

4. **Download Pre-trained Models**:
    The chatbot uses Hugging Face models for question generation and answer evaluation. Ensure the models are available by running:
    ```bash
    python -m transformers-cli download gpt2
    python -m transformers-cli download facebook/bart-large-mnli
    ```

5. **Run the Application**:
    To start the chatbot, run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

6. **Access the Application**:
    Once the application starts, open your web browser and navigate to `http://localhost:8501` to interact with the chatbot.

## Usage Guide

### Tech Stack Input:
- Use the sidebar to input the tech stack, including programming languages, frameworks, databases, and tools.
- You can enter the tech stack in a comma-separated format (e.g., `Python, JavaScript, React`).

### Interview Process:
1. **Question Generation**: The system generates 3 relevant interview questions for each technology from the provided tech stack.
2. **Answer Evaluation**: After answering each question, you can submit your response, and the system will evaluate it on a scale of 0 to 10 based on its correctness and relevance.
3. **Scoring**: The chatbot will calculate and display your total score based on all evaluated answers.

## Technical Details

- **Libraries Used**:
    - `streamlit`: Used for the web interface and creating an interactive dashboard.
    - `langchain`: A framework to integrate Hugging Face models for generating questions and evaluating answers.
    - `transformers`: Hugging Face’s library used to load and utilize pre-trained NLP models.
    - `pipeline`: Hugging Face's function to create pipelines for various tasks like text generation and classification.
  
- **Model Details**:
    - **Question Generation**: GPT-2 is used for generating interview questions related to the provided tech stack.
    - **Answer Evaluation**: BART (facebook/bart-large-mnli) is used for zero-shot classification to evaluate the relevance and correctness of the answers.

- **Architecture**:
    - The app is built using Streamlit for the frontend, Langchain for managing NLP prompts, and Hugging Face models for both question generation and answer evaluation.
    - The architecture allows flexibility in adding new models or modifying existing pipelines for question generation and answer scoring.

## Prompt Design

### Question Generation:
The prompt used for generating interview questions was designed to ensure that the generated questions are:
- **Technology-specific**: Questions are tailored to the technology stack provided by the user.
- **Diverse**: The generated questions cover different aspects of the technology to give a well-rounded interview.
  
Example of the question prompt:
```python
question_prompt_template = """
Generate exactly 3 interview questions related to the technology below:
Technology: {tech}
"""
