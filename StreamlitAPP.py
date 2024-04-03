import os
import PyPDF2
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.MCQGenerator import  generate_evaluate_chain
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from langchain.callbacks import get_openai_callback
# from langchain.llms import OpenAI 
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain, SequentialChain

import streamlit as st



with open(r"C:\Users\nutan\nutan\Gen AI\Project\Response.json", 'r') as file:
    RESPONSE_JSON = json.load(file)


st.title('MCQ creator App with langchain')

with st.form("user inputs"):

    upload_file = st.file_uploader("Upload a PDF or txt file")

    mcq_count = st.number_input("No of MCQs", min_value=3, max_value=50)

    subject = st.text_input("Insert subject", max_chars=20)

    tone = st.text_input("complexity level of Qustions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button(" Create MCQs")
    print("l3")
    if upload_file and button is not None and mcq_count and subject and tone:
        with st.spinner("loading...."):
            try:
                print("ll")
                text = read_file(upload_file)

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text":text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)

                        }
                    )

            except Exception as e:
                print("e1")
                traceback.print_exception(type(e), e, e.__traceback__)
                print(e)
                st.error("Error")

            else:
                print(f"Total tokens:{cb.total_tokens}","\n",
                        f"Promt tokens:{cb.prompt_tokens}","\n",
                        f"completion tokens : {cb.completion_tokens}","\n",
                        f"totsl cost: {cb.total_cost}")
                if isinstance(response, dict):

                    Quiz = response.get('quiz')
                    print(Quiz)
                    if Quiz is not None:
                        table_data = get_table_data(Quiz)
                        print(table_data)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index - df.index+1
                            st.table(df)

                            st.text_area(label = "Review", value=response["review"])
                        else:
                            st.error("Error in the table data")


                    else:
                        st.write(response)


