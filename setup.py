from setuptools import find_packages,setup

setup(
    name ='mcqgenratore',
    version= '0.0.1',
    author= 'Nutan_scienty',
    install_requires = ['openai', 'langchain', 'streamlit', 'python-dotenv', 'PyPDF2'],
    packages=find_packages()
)