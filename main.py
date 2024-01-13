# pip install streamlit <- webinterface
# pip install tiktoken <- counting tokens
# pip install openai <- accessing models

# pip install streamlit-extras
# https://www.buymeacoffee.com/doyouknowmarc

import tiktoken
import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
#import plotly.express as px



# vars
modelInputCost = 0
modelOutputCost = 0
num_input_tokens = 0
num_output_tokens = 0

# load encoder - encoder depends on the model
# https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
encoding = tiktoken.get_encoding("cl100k_base") # can be used for gpt-4, gpt-3.5-turbo, text-embedding-ada-002
used_encoding = "cl100k_base"
encoding = tiktoken.get_encoding(used_encoding)
input_encoding = 0
output_encoding = 0


# defs
def setModelCost(model_choice):
    global modelInputCost
    global modelOutputCost
    if model_choice == "gpt-3.5-turbo-1106":
        modelInputCost = 0.001 
        modelOutputCost = 0.002
    elif model_choice == "gpt-4":
        modelInputCost = 0.03
        modelOutputCost = 0.06
    elif model_choice == "gpt-4-32k":
        modelInputCost = 0.06
        modelOutputCost = 0.12
    elif model_choice == "gpt-4-1106-preview":
        modelInputCost = 0.01
        modelOutputCost = 0.03
            
    return model_choice

def calculateEverythingForBarChart(model_choice, text_input, text_output):
    global modelInputCost
    global modelOutputCost
    if model_choice == "gpt-3.5-turbo-1106":
        modelInputCost = 0.001 
        modelOutputCost = 0.002
        cost = calculateTotalCost(calculateInputCost(text_input), calculateOutputCost(text_output)) 
    elif model_choice == "gpt-4":
        modelInputCost = 0.03
        modelOutputCost = 0.06
        cost = calculateTotalCost(calculateInputCost(text_input), calculateOutputCost(text_output))
    elif model_choice == "gpt-4-32k":
        modelInputCost = 0.06
        modelOutputCost = 0.12
        cost = calculateTotalCost(calculateInputCost(text_input), calculateOutputCost(text_output))
    elif model_choice == "gpt-4-1106-preview":
        modelInputCost = 0.01
        modelOutputCost = 0.03
        cost = calculateTotalCost(calculateInputCost(text_input), calculateOutputCost(text_output))
            
    return "%0.7f" % cost

def calculateInputCost(text_input):
    global encoding
    global modelInputCost
    global input_encoding
    global num_input_tokens
    input_encoding = encoding.encode(text_input)
    num_input_tokens = len(encoding.encode(text_input))
    inputCost = num_input_tokens * modelInputCost / 1000
    return inputCost

def calculateOutputCost(text_output):
    global encoding
    global modelOutputCost
    global output_encoding
    global num_output_tokens
    output_encoding = encoding.encode(text_output)
    num_output_tokens = len(encoding.encode(text_output))
    outputCost = num_output_tokens * modelOutputCost / 1000
    return outputCost

def calculateTotalCost(calculatedInput, calculatedOutput):
    totalCost = calculatedInput + calculatedOutput
    return totalCost

def getEncoding(text):
    global encoding
    result = encoding.encode(text)
    return result

st.set_page_config(
        page_title="Token Cost Calculator",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.linkedin.com/in/doyouknowmarc/',
            'Report a bug': "https://www.linkedin.com/in/doyouknowmarc/",
            'About': "# Token Cost Calculator \n This application helps you to calculate the token costs associated with using LLMs from [OpenAI](https://openai.com/). This fun little calculator was developed by [Marc](https://www.linkedin.com/in/doyouknowmarc/). The motivation for this application is based on the recurring question I get during my job: \"how much does tokens cost?\". Further I'm trying to earn my very first dollar online."
        }
    )

tab1, tab2 = st.tabs(["Basic", "Advanced"])



st.sidebar.title("🚀 What is this App for?")
st.sidebar.write("To get a feeling of the associated token costs for using a LLM from [OpenAI](https://openai.com/) for various tasks.")
st.sidebar.markdown("1. **Input:** Enter your Prompt + any additional context as plain text (see example).")
st.sidebar.markdown("2. **Output:** Enter the expected response from the LLM.")
st.sidebar.header("📊 Configuration")
model_choice = st.sidebar.radio("Which model do you want to use?", ["gpt-3.5-turbo-1106", "gpt-4", "gpt-4-32k", "gpt-4-1106-preview"])

with st.sidebar.container():
    st.divider()
    st.image("Marc.png", use_column_width="never", width=100)
    st.header("Greetings 👋")
    st.write("My name is Marc and I'm trying to earn my very first dollar online as part of my New Year's resolution.")
    st.write("Will you help me? 🙈")
    button(username="doyouknowmarc", floating=False, width=220)
    st.write(f'Based on [OpenAI Pricing](https://openai.com/pricing) and [Tiktoken](https://github.com/openai/tiktoken)')
st.sidebar.container()

with tab1:
    st.title("Token Cost Calculator 💸")
    st.markdown(f'<p>The costs per 1000 Tokens based on <span style="color: rgb(255, 75, 75)">{setModelCost(model_choice)}</span> are <span style="color: rgb(255, 75, 75)">${modelInputCost}</span> for Input and <span style="color: rgb(255, 75, 75)">${modelOutputCost}</span> for Output.</p>', unsafe_allow_html=True)
    # columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Input")
        txt_input = st.text_area(label ="What will be send to the LLM? Enter the prompt + any additional context as plain text (see example).", height=185, placeholder="Classify for Invoice, Contract, Certificate. Return a JSON formated result containing a key called \"class\".\n### \nInvoice \nInvoice Number: #12345 \nDate: January 8, 2024 \nBill And Ship To: \nName: John Smith \nAddress: 123 Main Street \nCity/State: Anytown, CA 12345 \nPhone: (555) 123-4567 \nEmail: john.smith@email.com \nDescription of Products/Services: \nDescription - Quantity - Unit Price - Total \nProduct A - 2 - $50.00 - $100.00 \nProduct B - 3 - $30.00 - $90.00 \nSubtotal: $190.00 \nShipping: $10.00 \nTax (8%): $15.20 \nTotal Amount Due: $215.20 \nPayment Details: \nPayment Method: Credit Card \nPayment Due Date: January 22, 2024 \nThank you for your business! \n", value="Classify for Invoice, Contract, Certificate. Return a JSON formated result containing a key called \"class\".\n### \nInvoice \nInvoice Number: #12345 \nDate: January 8, 2024 \nBill And Ship To: \nName: John Smith \nAddress: 123 Main Street \nCity/State: Anytown, CA 12345 \nPhone: (555) 123-4567 \nEmail: john.smith@email.com \nDescription of Products/Services: \nDescription - Quantity - Unit Price - Total \nProduct A - 2 - $50.00 - $100.00 \nProduct B - 3 - $30.00 - $90.00 \nSubtotal: $190.00 \nShipping: $10.00 \nTax (8%): $15.20 \nTotal Amount Due: $215.20 \nPayment Details: \nPayment Method: Credit Card \nPayment Due Date: January 22, 2024 \nThank you for your business! \n")
        with st.expander("Show encoding of Input"):
            st.write(f'{getEncoding(txt_input)}')
        st.markdown(f'<p>Cost for input <span style="color: rgb(255, 75, 75);">${calculateInputCost(txt_input):.7f}</span> of {len(txt_input)} characters which represent {num_input_tokens} tokens.</p>', unsafe_allow_html=True)
        
    with col2:
        st.subheader("Output")
        txt_output = st.text_area(label="What will be the expected answer of the LLM? Enter it as plain text. See example: a JSON result containing key + value.", placeholder="{\n\"class\": \"Invoice\"\n}", value="{\n\"class\": \"Invoice\"\n}")
        with st.expander("Show encoding of Ouput"):
            st.write(f'{getEncoding(txt_output)}')
        st.markdown(f'<p style="text-align:right";>Cost for output <span style="color: rgb(255, 75, 75);">${calculateOutputCost(txt_output):.7f}</span> of {len(txt_output)} characters which represent {num_output_tokens} tokens.</p>', unsafe_allow_html=True)

    total = calculateTotalCost(calculateInputCost(txt_input), calculateOutputCost(txt_output))
    totaltokens = num_input_tokens + num_output_tokens
    st.markdown(f'<p style="text-align:center; font-weight: bold;"><span style="color: rgb(255, 75, 75); font-size: 24px">${total:.7f}</span></p>', unsafe_allow_html=True)
    st.write(f'<p style="text-align:center;">are the total costs for 1 query with {totaltokens} tokens when using <span style="color: rgb(255, 75, 75);">{model_choice}.</span></p>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("How much would 20 000 queries be? 🤔")
    values = st.slider(
    'Use the slider to see the minimum and maximum expected costs when doing 500 or even 100.000 queries.',
    500, 100000, (20000, 80000), step=500)
    
    minNewTotal = total * values[0]
    maxNewTotal = total * values[1]
    
    col3, col4 =st.columns(2)
    with col3:
        st.write(f'<p>The cost for <span style="color: rgb(255, 75, 75)">{values[0]}</span> queries when using <span style="color: rgb(255, 75, 75)">{model_choice}</span> would be <span style="color: rgb(255, 75, 75)">${minNewTotal:.2f}</span></p>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<p style="text-align:right;">The cost for <span style="color: rgb(255, 75, 75)">{values[1]}</span> queries when using <span style="color: rgb(255, 75, 75)">{model_choice}</span> would be <span style="color: rgb(255, 75, 75)">${maxNewTotal:.2f}</span></p>', unsafe_allow_html=True)


with tab2:
    st.write("Welcome to advanced mode")
    

#with tab3:
    # Data for the bar chart
    data = {'Model': ['gpt-3.5-turbo-1106', 'gpt-4', 'gpt-4-32k', 'gpt-4-1106-preview'],
            'cost in $': [calculateEverythingForBarChart('gpt-3.5-turbo-1106', txt_input, txt_output), calculateEverythingForBarChart('gpt-4', txt_input, txt_output), calculateEverythingForBarChart('gpt-4-32k', txt_input, txt_output), calculateEverythingForBarChart('gpt-4-1106-preview', txt_input, txt_output)]}
#asdf
    # Create a Streamlit app
 #   st.title("Total token cost by model bar chart")

    # Create a bar chart using Plotly
  #  fig = px.bar(data, x='Model', y='cost in $', text='cost in $', width=750, height=450, color=["green","blue","red","yellow"], color_discrete_sequence=["green","blue","red","yellow"], labels={'Category': 'Categories', 'Value': 'Values'})

    # Customize the chart (optional)
   # fig.update_layout(title="Total token cost by Model")
 #   fig.update_yaxes(tickprefix="$", showgrid=True)
    # Display the chart in Streamlit
 #   st.plotly_chart(fig)


# Day 1:
# Basic setup: installing python, setting up the environment, pip install streamlit, tiktoken, openai
# Building basic function: API Call to TIKTOKEN
# hardcoded pricing for one model according to the pricing page of OpenAI
# Making simple calculations based on the number of tokens and pricing
# Displaying costs - which changes when the text fields get other content
# MVP is working.

# Day 2:
# Adding a "BUY ME A COFFEE" Button.
# Adding a sidepanel with radio buttons (choose the model you want to use) as well as the BMAC Button
# Refactoring the code: sidepanel will now change the variables for the calculation
# Adding a little bit more explanation and styling

# Day 3:
# more explanations and a predefined template
# some UI improvements
# adding first advanced thing (show encoding and output)
# working with chatGPT to get some ideas on how to solve things .. but fallback to streamlit documentation
# adding a picture
# added 2 Links
# streamlit run main.py
# set page config
# comment in the community forum

# Day 4:
# further UI enhancements
# add slider for prognose of cost 500-100000 requests
# added a chart (not happy with it)

# Day 5:
# setup source control

# add detail mode (show encoding and single costs + token and character amount)
# add variance as a slider (%) for input and output - calculate if I have between -50% and + 200% more or less input / output
# add information page about tokens (4 characters are one token etc.)
# make it more relateable - add something like: for 100$ you could do X amount of calls


# Day 6:
# think about theming (color scheme)
#
#


# Day 7
#
#
#
# publish.