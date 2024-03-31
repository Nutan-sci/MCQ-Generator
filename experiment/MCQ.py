import os
import pandas
from langchain.chat_models import ChatOpenAI
import traceback
import json
from dotenv import load_dotenv
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
#my_key = "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"
#llm = ChatOpenAI(model_name = "gpt-3.4-turbo", temperature = 0.5)

print(KEY)