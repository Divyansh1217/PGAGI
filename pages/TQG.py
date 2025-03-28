import streamlit as st
import os
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import pipeline  # Hugging Face's pipeline

question_generator = pipeline("text-generation", model="gpt2",max_new_tokens=200)

huggingface_llm_question = HuggingFacePipeline(pipeline=question_generator)


answer_evaluator = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",max_length=100)

huggingface_llm_evaluation = HuggingFacePipeline(pipeline=answer_evaluator)

question_prompt_template = """
You are a helpful assistant that generates interview questions for technical topics. Based on the technology stack provided, generate 3 interview questions related to the technology.
Starts with Why?
Question1.
Question2.
Question3.
Technology: {tech}
"""


# Create a PromptTemplate instance for generating questions
question_template = PromptTemplate(input_variables=["tech"], template=question_prompt_template)

# Create an LLMChain instance for generating questions using Hugging Face model
llm_chain_question = LLMChain(llm=huggingface_llm_question, prompt=question_template)

# Define the prompt template for answer evaluation
evaluation_prompt_template = """
Evaluate the following answer to the question: "{question}"
Answer: "{answer}"
Grade the answer on a scale from 0 to 10 based on correctness and relevance.
Provide the score as a number only, without explanation.
"""

# Create a PromptTemplate instance for evaluation
evaluation_template = PromptTemplate(input_variables=["question", "answer"], template=evaluation_prompt_template)

# Create an LLMChain instance for evaluating answers using Hugging Face model
llm_chain_evaluation = LLMChain(llm=huggingface_llm_evaluation, prompt=evaluation_template)

# Function to generate interview questions for each technology
def generate_questions(tech_stack):
    questions = {}

    for tech in tech_stack:
        # Generate interview questions for the technology using the Hugging Face model
        generated_text = llm_chain_question.run(tech=tech)
        
        # Log the generated text for debugging
        st.write(f"Generated Text for {tech}: {generated_text}")
        
        # Clean the generated text by extracting only the questions
        # Assuming the questions are separated by line breaks or identifiable patterns
        extracted_questions = []
        for line in generated_text.split("\n"):
            # Check if the line looks like a question and add it to the list
            if "?" in line:
                extracted_questions.append(line.strip())

        # Ensure only 3 questions are selected
        questions[tech] = extracted_questions[:3]

    return questions

# Function to evaluate candidate's answers
def evaluate_answer(answer, question):
    """Evaluate candidate answers using Hugging Face model."""
    # Run the LLMChain to evaluate the answer based on the question
    response = llm_chain_evaluation.run(question=question, answer=answer)
    
    # Try parsing the response as a number
    try:
        score = float(response.strip())
        return round(score, 2) if 0 <= score <= 10 else 0.0
    except ValueError:
        return 0.0  # If the response cannot be converted to a valid score, return 0.0

# Streamlit UI for the interview process
def conduct_interview(tech_stack):
    """Streamlit UI for the interview process."""
    st.title("🧑‍💻 Technical Interview Questions Generator")

    # Generate questions for the selected tech stack
    questions = generate_questions(tech_stack)
    scores = {}
    total_score = 0

    for tech, q_list in questions.items():
        st.subheader(f"💡 {tech} Questions:")

        for i, question in enumerate(q_list):
            st.write(f"**Q{i+1}:** {question}")
            answer = st.text_area(f"Your Answer for {tech} - Q{i+1}", key=f"answer_{tech}_{i}")

            # Ensure each button has a unique key based on tech and question index
            button_key = f"submit_{tech}_{i}"
            if st.button(f"Submit Answer for {tech} - Q{i+1}", key=button_key):
                if answer.strip() == "":
                    st.warning("⚠️ Please enter an answer before submitting!")
                else:
                    # Evaluate the answer using the Hugging Face evaluation model
                    score = evaluate_answer(answer, question)
                    scores[f"{tech}_Q{i+1}"] = score
                    st.success(f"✅ Score: {score}/10")
                    total_score += score

    if scores:
        st.write(f"🎯 **Total Score: {total_score}/{len(scores) * 10}**")

# Tech Stack Input
st.sidebar.title("🔧 Select Your Tech Stack")
languages = st.sidebar.text_area("Programming Languages", "Python, JavaScript")
frameworks = st.sidebar.text_area("Frameworks", "Django, React")
databases = st.sidebar.text_area("Databases", "PostgreSQL, MongoDB")
tools = st.sidebar.text_area("Tools", "Docker, Kubernetes")

# Process Tech Stack
tech_stack = (
    [lang.strip() for lang in languages.split(",") if lang.strip()]
    + [fw.strip() for fw in frameworks.split(",") if fw.strip()]
    + [db.strip() for db in databases.split(",") if db.strip()]
    + [tl.strip() for tl in tools.split(",") if tl.strip()]
)

# Start Interview Button
if st.button("🚀 Start Interview"):
    conduct_interview(tech_stack)
