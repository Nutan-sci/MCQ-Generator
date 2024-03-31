import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
import traceback
import json
from dotenv import load_dotenv
load_dotenv()
#KEY = os.getenv("openai_api_key")

from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2
my_key = "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"

llm = ChatOpenAI(openai_api_key = my_key, model_name = "gpt-3.5-turbo", temperature = 0.5)

print(llm)
response_json = {
    "1":{
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        'correct': "correct answer"
    },
     "2":{
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        'correct': "correct answer"
    },
     "3":{
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here"
        },
        'correct': "correct answer"
    } 
}


TEMPLATE = """
Text:{text}
you are an expert MCQ maker. Given the above  text, it is your job to \
create a quiz of {number} multiple choice question for {subject} student in {tone} tone.
make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as guide. \
ensure to make {number} MSQS
### RESPONSE_JSON
{response_json}
             
"""

quiz_gen_prompt = PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE ,
)

quiz_chain = LLMChain(llm = llm, prompt =quiz_gen_prompt, output_key = 'quiz', verbose =True )

TEMPLATE2 ="""
You are an expert grammarian and writer. Given a Multiple Choice Quiz for {subject} student.\
you need to evaluate the complexity of the question and give a complete analysis of the quiz. only use at max 50 words for compleity 
if the quiz is not at per with cognitive and analytical abilities of the student.\
update the quiz qustions which needs to be changed and change the tone such that it perfectly fits the stidents availability
Quiz_MSQs:
{quiz}

Check form an expert English Writer of the above quiz
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=['subject', ' quiz'], template= TEMPLATE2)

#print(KEY)
review_chain = LLMChain(llm=llm, prompt = quiz_evaluation_prompt, output_key = "review", verbose = True)

generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain], input_variables = ['text', 'number', 'subject', 'tone','response_json'], 
                                          output_variables = ['quiz','review'], verbose =True)

file_path = r"C:\Users\nutan\nutan\Gen AI\Project\data.txt"
with open(file_path,'r') as file:
    TEXT = file.read()


#json.dumps(response_json)
NUMBER = 5
SUBJECT = 'MACHINE LEARNING'
TONE = "simple"

with get_openai_callback() as cb:
    response = generate_evaluate_chain(
        {
            "text":TEXT,
            "number": NUMBER,
            "subject": SUBJECT,
            "tone": TONE,
            "response_json": json.dumps(response_json)

        }
    )

print(f"Total tokens:{cb.total_tokens}","\n",
      f"Promt tokens:{cb.prompt_tokens}","\n",
      f"completion tokens : {cb.completion_tokens}","\n",
      f"totsl cost: {cb.total_cost}")

Quiz = response.get('quiz')

quiz = json.loads(Quiz)

quiz_table_data = []
for key, value in quiz.items():
    mcq = value['mcq']
    options = " | ".join(
        [
        f"{option}: {option_value}"
        for option , option_value in value['options'].items()
        ]
        )
    correct = value['correct']
    quiz_table_data.append({"MSQ":mcq, "Choice":options,'Correct':correct})
    
    quiz_df = pd.DataFrame(quiz_table_data)
    quiz_df.to_csv(r'C:\Users\nutan\nutan\Gen AI\Project\Machine_learning_MCQ.csv', index=False)