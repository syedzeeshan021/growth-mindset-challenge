import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.set_page_config(page_title="Properties of Common Solids", layout="wide")

# --- Theme Selection ---
theme = st.sidebar.radio("Select Theme", options=["Dark Mode", "Light Mode"])

if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            color: white;
        }
        .st-eb {
            background-color: #333333;
            color: white;
        }
        .st-bb {
            background-color: #444444;
            color: white;
        }
        .st-d3 {
            background-color: #555555;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ffffff;
            color: black;
        }
        .st-eb {
            background-color: #f0f0f0;
            color: black;
        }
        .st-bb {
            background-color: #e0e0e0;
            color: black;
        }
        .st-d3 {
            background-color: #d0d0d0;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Definitions Section ---
st.title("Properties of Common Solids")
st.subheader("Definitions")
st.markdown("""
**Melting Point:** The temperature at which a solid changes into a liquid.  
**Boiling Point:** The temperature at which a liquid changes into a gas.
""")
st.write("Below you can explore the properties of 10 common solids including their basic definitions (chemical name, history, and reserves) along with their melting and boiling points. You can also test your knowledge with an interactive quiz!")

# --- Data for 10 common solids ---
@st.cache_data(ttl=3600)
def load_solid_data():
    data = {
        "Solid": ["Iron", "Aluminum", "Copper", "Gold", "Silver", "Lead", "Zinc", "Tin", "Nickel", "Magnesium"],
        "Chemical Name": ["Fe", "Al", "Cu", "Au", "Ag", "Pb", "Zn", "Sn", "Ni", "Mg"],
        "History": [
            "Used since the Iron Age; abundant and crucial for tools and construction.",
            "Isolated in the 19th century; lightweight and widely used in industries.",
            "One of the oldest metals used by humans, valued for conductivity and malleability.",
            "Prized for its rarity and beauty, symbolizing wealth and status.",
            "Historically used in currency, jewelry, and art for centuries.",
            "Known for its malleability and density; used in batteries and construction.",
            "Essential for galvanizing and alloy production.",
            "Used since the Bronze Age, primarily as an alloying element.",
            "Valuable in stainless steel and corrosion-resistant alloys.",
            "A lightweight metal used in aerospace and automotive industries."
        ],
        "Total Reserve (World)": [
            "150 billion tonnes",
            "75 billion tonnes",
            "1 billion tonnes",
            "50,000 tonnes",
            "500,000 tonnes",
            "100 million tonnes",
            "250 million tonnes",
            "5 million tonnes",
            "80 million tonnes",
            "40 billion tonnes"
        ],
        "Reserve in Pakistan": [
            "2 billion tonnes",
            "500 million tonnes",
            "100 million tonnes",
            "Trace amounts",
            "Not significant",
            "10 million tonnes",
            "5 million tonnes",
            "Low reserves",
            "Limited reserves",
            "Moderate reserves"
        ],
        "Melting Point (°C)": [1538, 660, 1085, 1064, 961, 327, 419.5, 231.9, 1455, 650],
        "Boiling Point (°C)": [2862, 2519, 2562, 2856, 2162, 1749, 907, 2602, 2913, 1091]
    }
    df = pd.DataFrame(data)
    return df

solid_df = load_solid_data()

# --- Sidebar: Option to view full data (all solids) ---
st.sidebar.header("Options")
if st.sidebar.checkbox("Show full data table"):
    st.subheader("Full Data Table")
    st.dataframe(solid_df)

# --- Main Section: Display details of a selected solid ---
selected_solid = st.selectbox("Select a Solid", solid_df["Solid"].tolist())
selected_data = solid_df[solid_df["Solid"] == selected_solid].iloc[0]

st.subheader(f"Details for {selected_solid}")
st.markdown(f"""
**Chemical Name:** {selected_data['Chemical Name']}  
**History:** {selected_data['History']}  
**Total Reserve (World):** {selected_data['Total Reserve (World)']}  
**Reserve in Pakistan:** {selected_data['Reserve in Pakistan']}  
**Melting Point:** {selected_data['Melting Point (°C)']} °C  
**Boiling Point:** {selected_data['Boiling Point (°C)']} °C  
""")

# --- Temperature Conversion ---
def c_to_f(celsius):
    return (celsius * 9/5) + 32

st.subheader("Temperature Conversion")
if st.button("Convert Selected Solid Temperatures to Fahrenheit"):
    melting_f = c_to_f(selected_data['Melting Point (°C)'])
    boiling_f = c_to_f(selected_data['Boiling Point (°C)'])
    st.write(f"**Melting Point:** {melting_f:.2f} °F")
    st.write(f"**Boiling Point:** {boiling_f:.2f} °F")

# --- Quiz Section ---
st.header("Quiz: Test Your Knowledge!")
# Initialize session state for quiz control if not already set.
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

def generate_quiz_questions(num_questions=5):
    questions = []
    for _ in range(num_questions):
        row = solid_df.sample(1).iloc[0]
        solid = row["Solid"]
        # Randomly decide to quiz on melting or boiling point
        if random.choice([True, False]):
            q_text = f"What is the melting point (°C) of {solid}?"
            answer = row["Melting Point (°C)"]
        else:
            q_text = f"What is the boiling point (°C) of {solid}?"
            answer = row["Boiling Point (°C)"]
        questions.append({"question": q_text, "answer": answer})
    return questions

# Start or restart quiz
if not st.session_state.quiz_active:
    if st.button("Start Quiz"):
        st.session_state.quiz_questions = generate_quiz_questions(5)
        st.session_state.quiz_active = True

# Display quiz if active
if st.session_state.quiz_active:
    st.write("Answer the following questions (answers in °C):")
    with st.form("quiz_form"):
        user_answers = []
        for i, q in enumerate(st.session_state.quiz_questions):
            ans = st.text_input(f"Q{i+1}: {q['question']}", key=f"q{i}")
            user_answers.append(ans)
        submitted = st.form_submit_button("Submit Quiz")
    if submitted:
        score = 0
        results = []
        for i, q in enumerate(st.session_state.quiz_questions):
            try:
                user_val = float(user_answers[i])
            except:
                user_val = None
            correct_answer = q["answer"]
            # Allow a tolerance of 1 degree for a correct answer
            if user_val is not None and abs(user_val - correct_answer) < 1:
                score += 1
                results.append(f"Q{i+1}: Correct")
            else:
                results.append(f"Q{i+1}: Incorrect (Correct: {correct_answer} °C)")
        st.success(f"Your score: {score} out of {len(st.session_state.quiz_questions)}")
        for res in results:
            st.write(res)
        if st.button("Restart Quiz"):
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = []

# --- Preview Data Section ---
st.subheader("Data Preview")
preview = st.checkbox("Show preview of the selected solid's data before download")
if preview:
    # Show only the details for the currently selected solid.
    st.dataframe(solid_df[solid_df["Solid"] == selected_solid])

# --- Download Option ---
st.subheader("Download Solid Data")
if st.button("Download Data as Excel"):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        solid_df.to_excel(writer, sheet_name="Solids", index=False)
    buffer.seek(0)
    st.download_button(
        label="Download Excel",
        data=buffer,
        file_name="solids_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Footer
st.markdown("---")
st.markdown("Created by Syed Zeeshan Iqbal for educational purposes.")
