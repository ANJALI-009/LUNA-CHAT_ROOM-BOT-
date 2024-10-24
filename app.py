import streamlit as st
from phi.assistant import Assistant
from phi.llm.groq import Groq
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import pymysql
import os

# Load environment variables
load_dotenv()


# Fetch API key from environment variables
api_key = os.getenv("api_key")


# Add custom CSS for smoke background animation targeting stApp
st.markdown(
    """
    <style>
    /* Apply background smoke effect to the entire Streamlit app */
    .stApp {
        background-color: #1c1c1c;
        background-image: radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.15) 0%, rgba(0, 0, 0, 0) 50%), 
                          radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.15) 0%, rgba(0, 0, 0, 0) 50%);
                          background: linear-gradient(90deg, #0700b8 0%, #00ff88 100%);
        background-size: 400% 400%;
        animation: smokeAnimation 10s ease infinite;
        color: white;
    }

    /* Define the animation for the smoke */
    @keyframes smokeAnimation {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    /* Optional: Customize input box styles for better visibility */
    .stTextInput > div > input {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
    }

    /* Customize button styles */
    .stButton > button {
        background-color: #333;
        color: white;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to create MySQL connection
def create_mysql_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database="data"
        )
        return conn
    except pymysql.MySQLError as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Initialize the assistant
@st.cache_resource
def get_assistant():
    return Assistant(
        llm=Groq(model="llama-3.1-70b-versatile", api_key=api_key),
        description="I am a helpful AI assistant powered by Groq. How can I assist you today?",
    )

# Function to fetch data from MySQL
def fetch_trainer_data():
    conn = create_mysql_connection()
    if conn is None:
        return []  # Return an empty list if connection failed
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, domain, skills, experience, links FROM persons")
        records = cursor.fetchall()
        return records
    except pymysql.MySQLError as e:
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Function to generate embeddings using SentenceTransformer
@st.cache_resource
def generate_embeddings(data):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = []
    ids = []
    
    for record in data:
        person_id, name, domain, skills, experience = record[:5]
        description = f"{name}, {experience} years of experience, skilled in {skills}, and works in {domain}."
        embedding = model.encode(description)
        ids.append(person_id)
        embeddings.append(embedding)
    
    return ids, np.array(embeddings)

# Function to build FAISS index
@st.cache_resource
def build_faiss_index(embeddings):
    if len(embeddings.shape) == 2:
        dimension = embeddings.shape[1]
        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_index.add(embeddings)
        return faiss_index
    else:
        raise ValueError(f"Expected embeddings to be a 2D array, but got shape {embeddings.shape}")

# Function to perform FAISS search
def search_in_faiss(index, query_embedding, top_k=3):
    distances, indices = index.search(query_embedding, top_k)
    return distances, indices

# Function to create a clickable button for each trainer
def create_trainer_button(trainer_name, link):
    st.markdown(f'<a href="{link}" target="_blank"><button style="background-color:#4CAF50; color:white; padding:10px; border:none; border-radius:4px; cursor:pointer;">Chat with {trainer_name}</button></a>', unsafe_allow_html=True)

# Streamlit app
st.title("LUNA CHAT_ROOM BOT")

# Input text box for user question
user_input = st.text_input("How can I help you ?")

# Generate embedding for the user query outside the button click logic
model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode([user_input]) if user_input.strip() else None

# Button to get the response
if st.button("Ask"):
    if user_input.strip():
        with st.spinner("Generating response..."):
            response_generator = get_assistant().chat(user_input)
            response = "".join([chunk for chunk in response_generator if isinstance(chunk, str)])
            st.markdown(response)

            # Fetch trainer data from MySQL
            trainer_data = fetch_trainer_data()

            # Generate embeddings from database data
            ids, embeddings = generate_embeddings(trainer_data)

            # Build FAISS index with embeddings
            try:
                faiss_index = build_faiss_index(embeddings)
            except ValueError as e:
                st.error(f"Error: {e}")
                faiss_index = None

            if faiss_index and query_embedding is not None:
                distances, indices = search_in_faiss(faiss_index, np.array(query_embedding))

                # Display matched results from database
                st.markdown("### Related Trainers from Database:")
                for idx in indices[0]:
                    person_id, name, domain, skills, experience, link = trainer_data[idx]
                    st.markdown(f"- *Name: {name}, **Domain: {domain}, **Skills: {skills}, **Experience*: {experience} years")
                    create_trainer_button(name, link)
    else:
        st.warning("Please enter a question.")




