import streamlit as st
import pandas as pd
import random
from io import BytesIO

# Page configuration with a unique title and wide layout
st.set_page_config(page_title="Properties of Common Solids - Educational Demo", layout="wide")

# Sidebar: Theme selection
selected_theme = st.sidebar.radio("Select Display Theme:", ["Light Mode", "Dark Mode"])
if selected_theme == "Dark Mode":
    st.markdown(
        """
        <style>
        .stApp { background-color: #121212; color: #e0e0e0; }
        .stDataFrame, .stButton { background-color: #1f1f1f; color: #e0e0e0; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #ffffff; color: #333333; }
        .stDataFrame, .stButton { background-color: #f8f8f8; color: #333333; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Introduction Section ---
st.title("Educational Exploration: Properties of Common Solids")
st.subheader("Fundamental Definitions")
st.markdown("""
- **Melting Point:** Temperature at which a solid turns into a liquid.
- **Boiling Point:** Temperature at which a liquid turns into a gas.
- **Chemical Name:** The scientific symbol representing the element.
- **Atomic Number:** Number of protons in an atom, which identifies the element.
""")
st.write("Explore the properties of 10 common solids including their chemical details, historical significance, and temperature thresholds. Test your knowledge with the interactive quiz below!")

# --- Data for 10 Common Solids ---
@st.cache_data(ttl=3600)
def load_solids():
    data = {
        "Solid": ["Iron", "Aluminum", "Copper", "Gold", "Silver", "Lead", "Zinc", "Tin", "Nickel", "Magnesium"],
        "Chemical Name": ["Fe", "Al", "Cu", "Au", "Ag", "Pb", "Zn", "Sn", "Ni", "Mg"],
        "Atomic Number": [26, 13, 29, 79, 47, 82, 30, 50, 28, 12],
        "Short History": [
            "Used since the Iron Age; critical for construction and tools.",
            "Discovered in the 19th century; known for its lightweight and corrosion resistance.",
            "Valued for conductivity and malleability since ancient times.",
            "Admired for rarity and luster, symbolizing wealth and power.",
            "Historically used in currency, jewelry, and ornamental items.",
            "Known for its density and malleability; used in batteries and shielding.",
            "Important for galvanizing and alloy creation.",
            "Historically used since the Bronze Age; prevalent in alloys.",
            "Essential for producing stainless steel and corrosion-resistant materials.",
            "A lightweight metal significant in aerospace and automotive engineering."
        ],
        "Total Reserve (World)": [
            "150 billion tonnes", "75 billion tonnes", "1 billion tonnes", "50,000 tonnes",
            "500,000 tonnes", "100 million tonnes", "250 million tonnes", "5 million tonnes",
            "80 million tonnes", "40 billion tonnes"
        ],
        "Reserve in Pakistan": [
            "2 billion tonnes", "500 million tonnes", "100 million tonnes", "Trace amounts",
            "Not significant", "10 million tonnes", "5 million tonnes", "Low reserves",
            "Limited reserves", "Moderate reserves"
        ],
        "Melting Point (°C)": [1538, 660, 1085, 1064, 961, 327, 419.5, 231.9, 1455, 650],
        "Boiling Point (°C)": [2862, 2519, 2562, 2856, 2162, 1749, 907, 2602, 2913, 1091]
    }
    return pd.DataFrame(data)

solids_df = load_solids()

# --- Sidebar Option: Display Full Data ---
st.sidebar.header("Data Options")
if st.sidebar.checkbox("Show complete dataset"):
    st.subheader("Complete Solids Data")
    st.dataframe(solids_df)

# --- Function to Create Wikipedia Link ---
def create_wikipedia_link(solid):
    if solid == "Aluminum":
        return "https://en.wikipedia.org/wiki/Aluminium"
    else:
        return f"https://en.wikipedia.org/wiki/{solid}"

# --- Main Section: Display Details of the Selected Solid ---
selected_solid = st.selectbox("Choose a Solid", solids_df["Solid"].tolist())
selected_info = solids_df[solids_df["Solid"] == selected_solid].iloc[0]

st.subheader(f"Details for {selected_solid}")
st.markdown(f"""
**Chemical Symbol:** {selected_info['Chemical Name']}  
**Atomic Number:** {selected_info['Atomic Number']}  
**Historical Overview:** {selected_info['Short History']}  

**Global Reserve:** {selected_info['Total Reserve (World)']}  
**Reserve in Pakistan:** {selected_info['Reserve in Pakistan']}  
**Melting Point:** {selected_info['Melting Point (°C)']} °C  
**Boiling Point:** {selected_info['Boiling Point (°C)']} °C  
""")
wiki_url = create_wikipedia_link(selected_solid)
st.markdown(f'<a href="{wiki_url}" target="_blank">Learn more about {selected_solid} on Wikipedia</a>', unsafe_allow_html=True)

# --- Temperature Conversion: Celsius to Fahrenheit ---
def convert_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

st.subheader("Temperature Conversion Tool")
if st.button("Convert Temperatures to Fahrenheit"):
    melting_f = convert_to_fahrenheit(selected_info['Melting Point (°C)'])
    boiling_f = convert_to_fahrenheit(selected_info['Boiling Point (°C)'])
    st.write(f"**Melting Point:** {melting_f:.2f} °F")
    st.write(f"**Boiling Point:** {boiling_f:.2f} °F")

# ==========================
# --- Quiz Section ---
# ==========================
st.header("Quiz: Test Your Knowledge!")

# Initialize quiz state variables if not already present
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

# Helper function to create multiple-choice options
def create_options(row, q_type, correct_answer):
    column = {
        "melting": "Melting Point (°C)",
        "boiling": "Boiling Point (°C)",
        "chemical": "Chemical Name",
        "atomic": "Atomic Number",
        "reserve": "Total Reserve (World)",
        "reserve_pakistan": "Reserve in Pakistan"
    }[q_type]
    distractors = solids_df[solids_df[column] != correct_answer][column].unique().tolist()
    if len(distractors) >= 3:
        distractors = random.sample(distractors, 3)
    options = distractors + [correct_answer]
    options = [str(opt) for opt in options]
    random.shuffle(options)
    return options

# Function to generate quiz questions
def generate_quiz(num=6):
    quiz = []
    question_types = ["melting", "boiling", "chemical", "atomic", "reserve", "reserve_pakistan"]
    for _ in range(num):
        row = solids_df.sample(1).iloc[0]
        solid = row["Solid"]
        q_type = random.choice(question_types)
        if q_type == "melting":
            q_text = f"What is the melting point (°C) of {solid}?"
            answer = row["Melting Point (°C)"]
        elif q_type == "boiling":
            q_text = f"What is the boiling point (°C) of {solid}?"
            answer = row["Boiling Point (°C)"]
        elif q_type == "chemical":
            q_text = f"What is the chemical symbol of {solid}?"
            answer = row["Chemical Name"]
        elif q_type == "atomic":
            q_text = f"What is the atomic number of {solid}?"
            answer = row["Atomic Number"]
        elif q_type == "reserve":
            q_text = f"What is the total reserve (world) of {solid}?"
            answer = row["Total Reserve (World)"]
        elif q_type == "reserve_pakistan":
            q_text = f"What is the reserve in Pakistan of {solid}?"
            answer = row["Reserve in Pakistan"]
        options = create_options(row, q_type, answer)
        quiz.append({"question": q_text, "answer": answer, "options": options})
    return quiz

# Start quiz if not already active
if not st.session_state.quiz_active:
    if st.button("Start Quiz"):
        st.session_state.quiz_questions = generate_quiz(6)
        st.session_state.quiz_active = True
        st.session_state.current_question_index = 0
        st.session_state.quiz_score = 0
        st.rerun()

# Display quiz questions using a dynamic form-based UI
if st.session_state.quiz_active:
    idx = st.session_state.current_question_index
    total = len(st.session_state.quiz_questions)
    if idx < total:
        current_q = st.session_state.quiz_questions[idx]
        with st.form(key=f"quiz_form_{idx}", clear_on_submit=True):
            st.markdown(f"### **Question {idx + 1}:** {current_q['question']}")
            selected_option = st.radio("Select your answer:", current_q["options"], key=f"quiz_radio_{idx}")
            submitted = st.form_submit_button("Submit Answer")
        # If form is submitted, store a flag in session_state for this question.
        if submitted:
            if selected_option == str(current_q["answer"]):
                st.success("Correct!")
                st.session_state.quiz_score += 1
            else:
                st.error(f"Incorrect. The correct answer is: {current_q['answer']}")
            st.session_state[f"submitted_{idx}"] = True
        # Show Next Question button only if answer is submitted.
        if st.session_state.get(f"submitted_{idx}", False):
            if st.button("Next Question"):
                st.session_state.current_question_index += 1
                # Clear the submitted flag for the current question.
                st.session_state.pop(f"submitted_{idx}", None)
                st.rerun()
    else:
        st.success("Quiz Completed!")
        st.write(f"Your final score is: {st.session_state.quiz_score} out of {total}")
        if st.button("Restart Quiz"):
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = []
            st.session_state.current_question_index = 0
            st.session_state.quiz_score = 0
            # Remove any submission flags.
            keys = list(st.session_state.keys())
            for key in keys:
                if key.startswith("submitted_"):
                    st.session_state.pop(key)
            st.experimental_rerun()

# --- Data Preview and Download Section ---
st.subheader("Data Preview for the Selected Solid")
if st.checkbox("Preview Data"):
    st.dataframe(solids_df[solids_df["Solid"] == selected_solid])

st.subheader("Download the Solids Data")
if st.button("Download as Excel"):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        solids_df.to_excel(writer, sheet_name="Solids", index=False)
    buffer.seek(0)
    st.download_button(
        label="Download Excel File",
        data=buffer,
        file_name="solids_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Footer ---
st.markdown("---")
st.markdown("Created by Syed Zeeshan Iqbal for educational purposes. This unique version is intended for learning and demonstration.")
