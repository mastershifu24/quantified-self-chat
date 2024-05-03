import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
import base64

# Set the environment variable
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]


def configure_model():
    """Configure the generative model."""
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    return genai.GenerativeModel('gemini-pro')

def load_data(file_path, columns_to_keep):
    """Load and preprocess the data."""
    df = pd.read_csv(file_path, delimiter=',')
    df = df[columns_to_keep]  # Select only the desired columns
    return df.to_dict(orient='list')

def get_response(model, user_input, sleep_data):
    """Generate a response from the model."""
    input_prompt = f"This is user asking : {user_input}\n\n based on what user asked, this is the sleep data: {str(sleep_data)}\n\n Give me short quantified answer in 1 to 5 lines only based on the sleep data: "
    return model.generate_content(input_prompt).text

def main():
    """Main function to run the app."""
    st.title('The Quantified Self Chat')
    model = configure_model()
    columns_to_keep = ['Column1', 'Column2', 'Column3']  # Specify the columns you want to keep
    sleep_data = load_data('sleep_data.csv', columns_to_keep)

    st.subheader('Sleep dataset')
    st.write(pd.DataFrame.from_dict(sleep_data))

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = st.text_input("Ask Questions", "")

    if st.button("Submit") and user_input.strip():  # Check if user input is not empty
        response = get_response(model, user_input, sleep_data)

        # Update chat history
        st.session_state['chat_history'].append({"User": user_input, "Gemini Pro": response})

    # Display chat history
    for chat in st.session_state['chat_history']:
        st.write(f"User: {chat['User']}")
        st.write(f"Gemini Pro: {chat['Gemini Pro']}")

if __name__ == "__main__":
    main()
