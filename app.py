import pandas as pd
import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Load the text data
file_path = 'official_ chatbot.csv'
text_data = pd.read_csv(file_path)

# Initialize the OpenAI model
api_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_key=api_key)

# Define the prompt template for health statistics data
prompt_template = PromptTemplate(
    input_variables=["data_description", "question"],
    template="""
    You are a chatbot for Sir Lester Bird Medical Center, who is providing info to people going into surgeries and so you are very empathetic and professional. You complete all your sentences. You stick to the data ONLY. You do not make up fake prices. You keep your answers really short. You keep your answers straight to the point. You keep all your answers to one line. You give information concerning only Antigua and Barbuda. You have access to the following surgery data:
    {data_description}

    Question: {question}

    Please provide a detailed answer based on the data.
    """
)

# Create the LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Function to generate data description for the health statistics
def generate_data_description():
    sample_entries = text_data.sample(min(len(text_data), 5))  # Get up to 5 random rows
    description = "The dataset contains various info on the SLBMC surgery types over different years. It includes data points such as Surgery options, Surgery pricing, Preparation for surgeries, and Reasons why surgeries are done. The data is structured with the following columns:\n"
    description += "- Keywords: The word which provides the info on surgeries.\n"
    description += "- Responses: The info on surgeries.\n"
    description += "Example entries:\n"
    description += "\n".join(f"Keywords {row['Keywords:']}, Responses {row['Responses:']}," for _, row in sample_entries.iterrows())
    return description

def get_response(question):
    data_description = generate_data_description()
    response = chain.run(data_description=data_description, question=question)
    return response

# Streamlit UI
st.title("MedAssist Chatbot")
st.write("DISCLAIMER: This chatbot is not created by certified doctors! The information provided in this chatbot is only applicable for Sir Lester Bird Medical Center in Antigua. Ask any questions related to surgeries and procedures based on available data.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Ensure 'messages' is initialized

# Function to add messages to the chat history
def add_message(sender, message):
    st.session_state["messages"].append({"sender": sender, "message": message})
    
# Function to display messages with an icon
def display_message(message, icon):
    st.markdown(f"<div style='display: flex; align-items: center;'>"
                 f"<img src='{icon}' alt='icon' style='width: 20px; height: 20px; margin-right: 10px;'>"
                 f"<span>{message}</span></div>",
                 unsafe_allow_html=True)

# Icon URL (Make sure to use a valid URL or local path to an image)
chatbot_icon = "https://www.dropbox.com/scl/fi/hys25ooo4tfh8zftt0r1q/single_logo-removebg-preview.png?rlkey=3vkem1agmpmu8kqypezp8hghq&st=rohhzsos&dl=0"  # Replace with your icon URL
user_icon = "https://www.dropbox.com/scl/fi/pti8v2bx8ewcr046lw4mf/user_logo-removebg-preview.png?rlkey=7q9otj7vogdq4sbxbvi8swbny&st=zhsemrnu&dl=0"        # Replace with your icon URL

# Handle user input
user_input = st.chat_input("Type your question on surgeries (or type bye to quit):")

if user_input:
    # Add the user's message to the chat
    add_message("user", user_input)
    
    # Get the AI response
    response = get_response(user_input)
    
    # Add the AI response to the chat
    add_message("ai", response)

# Display the chat history
if "messages" in st.session_state:  # Double-check that 'messages' exists
    for chat in st.session_state["messages"]:
        with st.chat_message(chat["sender"]):
            st.write(chat["message"])


# Add a sidebar header
st.sidebar.header("Sidebar Menu")

# Add some widgets to the sidebar
option = st.sidebar.selectbox("Select an option:", ["Option 1", "Option 2", "Option 3"])

# Display the selected option in the main area
st.write(f"You selected: {option}")

# You can also add other widgets like sliders, checkboxes, etc.
if st.sidebar.checkbox("Show additional information"):
    st.sidebar.write("Here is some additional information!")
