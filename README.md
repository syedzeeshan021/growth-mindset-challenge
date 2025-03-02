# growth-mindset-challenge
# Properties of Common Solids - Interactive Streamlit App

## About this Project
This project is an interactive web application built with Streamlit that allows users to explore the physical properties of common solids. The app provides detailed information on each solid, including:
- **Chemical Name**  
- **History** (a brief overview of the solid's usage and significance)  
- **Total Reserves in the World**  
- **Reserves in Pakistan**  
- **Melting Point**  
- **Boiling Point**

In addition to presenting these properties, the app offers interactive features such as temperature conversion and a quiz to test your knowledge about these solids.

## Features
- **Interactive Solid Details:**  
  Select a solid from the dropdown menu to view its comprehensive details (chemical name, history, reserves, melting & boiling points).

- **Temperature Conversion:**  
  Easily convert melting and boiling points from Celsius to Fahrenheit with a click of a button.

- **Interactive Quiz:**  
  Challenge yourself with a 5-question quiz that randomly asks about the melting or boiling points of various solids. Get instant feedback and see your final score.

- **Theme Selection:**  
  Choose between Dark Mode and Light Mode via the sidebar for a customized viewing experience.

- **Data Preview & Download:**  
  Preview the details of the selected solid before downloading the complete dataset as an Excel file.

## Technologies Used
- **Python:** The main programming language used to build the app.
- **Streamlit:** A powerful framework for creating interactive web apps quickly.
- **Pandas:** Used for data manipulation and management.
- **XlsxWriter:** Enables exporting data to Excel files.
- **HTML/CSS:** Custom styling is applied to support both dark and light themes.
- **Random:** Python's built-in module for generating random quiz questions.

## How to Run the App
1. **Install Python 3.x:**  
   Ensure that you have Python 3.x installed on your machine.

2. **Install Dependencies:**  
   Use pip to install the necessary packages:

   pip install streamlit pandas xlsxwriter

3. **Run the App:**
Navigate to the project directory and run:

  streamlit run app.py
  
4. **Interact with the App:**

  Use the sidebar to switch between Dark Mode and Light Mode.
  Select a solid to view its details.
  Convert temperatures or take the quiz.
  Preview data for the selected solid before downloading the full dataset.
5. **Project Structure:**

  app.py: The main Python file containing the Streamlit application code.
  README.md: This file, which provides an overview of the project and instructions for running the app.
  Assets (if any): Additional files such as images or style sheets.
6. **Contribution:**

  Contributions, issues, and feature requests are welcome! Feel free to fork this project and submit pull requests.

  Enjoy exploring the properties of common solids and have fun testing your knowledge with this interactive app!

  This README provides a comprehensive overview of the project, its features, and how to run it,
