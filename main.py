import tiktoken
import streamlit as st
# from streamlit_extras.buy_me_a_coffee import button

# vars
modelInputCost = 0
modelOutputCost = 0
num_input_tokens = 0
num_output_tokens = 0
inputCost = 0
outputCost = 0

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
    global inputCost
    input_encoding = encoding.encode(text_input)
    num_input_tokens = len(encoding.encode(text_input))
    inputCost = num_input_tokens * modelInputCost / 1000
    return inputCost


def calculateOutputCost(text_output):
    global encoding
    global modelOutputCost
    global output_encoding
    global num_output_tokens
    global outputCost
    output_encoding = encoding.encode(text_output)
    num_output_tokens = len(encoding.encode(text_output))
    outputCost = num_output_tokens * modelOutputCost / 1000
    return outputCost

def calculateTotalCost(calculatedPrompt, calculatedInput, calculatedOutput):
    totalCost = calculatedPrompt + calculatedInput + calculatedOutput
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
            'Report a bug': "https://github.com/doyouknowmarc/tokencostcalculator/issues",
            'About': "# Token Cost Calculator \n This application helps you to calculate the token costs associated with using LLMs from [OpenAI](https://openai.com/). This fun little calculator was developed by [Marc](https://www.linkedin.com/in/doyouknowmarc/). The motivation for this application is based on the recurring question I get during my job: \"how much does tokens cost?\". Further I'm trying to earn my very first dollar online."
        }
    )


st.sidebar.title("🚀 What is this App for?")
st.sidebar.write("To get a feeling of the associated token costs for using a LLM from [OpenAI](https://openai.com/) for various tasks.")
st.sidebar.markdown("1. **Prompt:** What should the LLM do?")
st.sidebar.markdown("2. **Input:** Content / context as plain text.")
st.sidebar.markdown("3. **Output:** Expected LLM response.")
st.sidebar.write("This app will NOT perform an actual request. You need to enter your content in every field. You could copy paste Prompt, Input and Output from chatGPT for example.")
st.sidebar.divider()
st.sidebar.header("📊 Configuration")
model_choice = st.sidebar.radio("Which model do you want to use?", ["gpt-3.5-turbo-1106", "gpt-4", "gpt-4-32k", "gpt-4-1106-preview"])
st.sidebar.divider()
st.sidebar.subheader("🤓 Detail Mode")
st.sidebar.write("If you are interessted in the encodings, number of tokens, number of characters, individual costs and simply more options activate the folowing:")
detailMode = st.sidebar.checkbox('Show me more details 🤓')

with st.sidebar.container():
    st.divider()
    st.image("Marc.png", use_column_width="never", width=100)
    st.header("Greetings 👋")
    st.write("My name is Marc and I'm trying to earn my very first dollar online as part of my New Year's resolution.")
    st.write("Will you [help](https://ko-fi.com/doyouknowmarc) me? 🙈")
   # button(username="doyouknowmarc", floating=False, width=220)
    st.write(f'Based on [OpenAI Pricing](https://openai.com/pricing) and [Tiktoken](https://github.com/openai/tiktoken)')
    



st.title("Token Cost Calculator 💸")
st.markdown(f'<p>The costs per 1000 Tokens based on <span style="color: rgb(255, 75, 75)">{setModelCost(model_choice)}</span> are <span style="color: rgb(255, 75, 75)">${modelInputCost}</span> for Input and <span style="color: rgb(255, 75, 75)">${modelOutputCost}</span> for Output.</p>', unsafe_allow_html=True)

# columns
col1, col2 = st.columns(2)
with col1:
    st.subheader("Prompt")
    txt_prompt = st.text_area(label ="What is the task? Enter the prompt (see example).", placeholder="Classify for Invoice, Contract, Certificate.\nReturn a JSON formated result containing a key called \"class\".",value="Classify for Invoice, Contract, Certificate.\nReturn a JSON formated result containing a key called \"class\".")
    if detailMode:
        with st.expander("Show encoding of Prompt"):
            st.write(f'{getEncoding(txt_prompt)}')
        st.markdown(f'<p>Cost for prompt <span style="color: rgb(255, 75, 75);">${calculateInputCost(txt_prompt):.7f}</span> of {len(txt_prompt)} characters which represent {num_input_tokens} tokens.</p>', unsafe_allow_html=True)

    st.subheader("Input")
    txt_input = st.text_area(label ="What content will be send to the LLM? Enter the Input / context as plain text (see example).", height=185, placeholder="### \nInvoice \nInvoice Number: #12345 \nDate: January 8, 2024 \nBill And Ship To: \nName: John Smith \nAddress: 123 Main Street \nCity/State: Anytown, CA 12345 \nPhone: (555) 123-4567 \nEmail: john.smith@email.com \nDescription of Products/Services: \nDescription - Quantity - Unit Price - Total \nProduct A - 2 - $50.00 - $100.00 \nProduct B - 3 - $30.00 - $90.00 \nSubtotal: $190.00 \nShipping: $10.00 \nTax (8%): $15.20 \nTotal Amount Due: $215.20 \nPayment Details: \nPayment Method: Credit Card \nPayment Due Date: January 22, 2024 \nThank you for your business! \n", value="### \nInvoice \nInvoice Number: #12345 \nDate: January 8, 2024 \nBill And Ship To: \nName: John Smith \nAddress: 123 Main Street \nCity/State: Anytown, CA 12345 \nPhone: (555) 123-4567 \nEmail: john.smith@email.com \nDescription of Products/Services: \nDescription - Quantity - Unit Price - Total \nProduct A - 2 - $50.00 - $100.00 \nProduct B - 3 - $30.00 - $90.00 \nSubtotal: $190.00 \nShipping: $10.00 \nTax (8%): $15.20 \nTotal Amount Due: $215.20 \nPayment Details: \nPayment Method: Credit Card \nPayment Due Date: January 22, 2024 \nThank you for your business! \n")
    
    if detailMode:
        with st.expander("Show encoding of Input"):
            st.write(f'{getEncoding(txt_input)}')
        st.markdown(f'<p>Cost for input <span style="color: rgb(255, 75, 75);">${calculateInputCost(txt_input):.7f}</span> of {len(txt_input)} characters which represent {num_input_tokens} tokens.</p>', unsafe_allow_html=True)
    
    st.subheader("Output")
    txt_output = st.text_area(label="What will be the expected answer of the LLM? Enter it as plain text. See example: a JSON result containing key + value.", placeholder="{\n\"class\": \"Invoice\"\n}", value="{\n\"class\": \"Invoice\"\n}")
    
    if detailMode:
        with st.expander("Show encoding of Ouput"):
            st.write(f'{getEncoding(txt_output)}')
        st.markdown(f'<p>Cost for output <span style="color: rgb(255, 75, 75);">${calculateOutputCost(txt_output):.7f}</span> of {len(txt_output)} characters which represent {num_output_tokens} tokens.</p>', unsafe_allow_html=True)


# calcs
total = calculateTotalCost(calculateInputCost(txt_prompt), calculateInputCost(txt_input), calculateOutputCost(txt_output))
totaltokens = num_input_tokens + num_output_tokens + len(encoding.encode(txt_prompt))

prompt_prozent = calculateInputCost(txt_prompt) / total * 100
input_prozent = calculateInputCost(txt_input) / total * 100
output_prozent = calculateOutputCost(txt_output) / total * 100
onehundreddollar = 100/total
prompt_plus_input_percent = prompt_prozent + input_prozent
prompt_plus_input_cost = calculateInputCost(txt_prompt) + calculateInputCost(txt_input)
output_cost = calculateOutputCost(txt_output)

with col2:
    st.subheader("Result")
    st.write(f'<p>The total costs for 1 query with {totaltokens} tokens when using <span style="color: rgb(255, 75, 75);">{model_choice}</span> are: </p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; font-weight: bold;"><span style="color: rgb(255, 75, 75); font-size: 32px">${total:.7f}</span></p>', unsafe_allow_html=True)
    st.divider()
    st.write(f'If you want to see more details <span style="color: rgb(255, 75, 75);">consider activating "Detail Mode"</span> in the sidepanel / menu. The additional content will be right below the input fields as well as at the bottom of the page.', unsafe_allow_html=True)
    st.write(f'Detail Mode includes:')
    st.markdown("""
                * Individual attributed costs for Prompt, Input and Output.
                * Encoding for Prompt, Input and Output as well as processed characters and corresponding Tokens
                * Cost distribution in percent
                * Option to enter a min and max range of queries you would like to do + the associated costs
                * Seeing how much queries you could send with 100$ based on your prompt
                * Option to enter you own budget and see how many queries you could do yearly / per day
                * Option to freely adjust the min. and max. Prompt, Input and Output Tokens + the associated costs to that regarding 1 query or multiple.
                """)
    
st.divider()
if detailMode: 
    a, b, c = st.columns(3)
    with a:
        st.subheader("Cost distribution in percent for your query")
        st.write(f'<p>Prompt: <span style="color: rgb(255, 75, 75);">{prompt_prozent:.2f}%</span></p>', unsafe_allow_html=True)
        st.write(f'<p>Input: <span style="color: rgb(255, 75, 75);">{input_prozent:.2f}%</span></p>', unsafe_allow_html=True)
        st.write(f'<p>Output: <span style="color: rgb(255, 75, 75);">{output_prozent:.2f}%</span> </p>', unsafe_allow_html=True)
        st.write(f'<p>Which means that your call to the LLM (Prompt + Input) is responsible for: <span style="color: rgb(255, 75, 75);">{prompt_plus_input_percent:.2f}%</span> of the costs or <span style="color: rgb(255, 75, 75);">{prompt_plus_input_cost:.7f}$</span> where as the Output contributes to <span style="color: rgb(255, 75, 75);">{output_prozent:.2f}%</span> or <span style="color: rgb(255, 75, 75);">{output_cost:.7f}$</span>. This may help you to identify saving opportunities.</p>', unsafe_allow_html=True)
    with b:
        st.subheader("100$")
        st.markdown(f'<p>A budget of 100$ would suffice for: <span style="color: rgb(255, 75, 75);">{onehundreddollar:.0f} such queries</span></p>', unsafe_allow_html=True)
    with c:
        st.subheader("Based on your budget")
        your_budget = st.number_input('Insert your budget in $',value=2000)
        result_your_budget = your_budget/total
        daily_queries_based_on_your_budget = result_your_budget / 250
        st.markdown(f'<p>Would result in: <span style="color: rgb(255, 75, 75);">{result_your_budget:.0f} such queries</span></p>', unsafe_allow_html=True)
        st.write(f'<p>If <span style="color: rgb(255, 75, 75);">{your_budget:.0f} $</span> is your <span style="color: rgb(255, 75, 75);">yearly</span> budget this would enable you to do <span style="color: rgb(255, 75, 75);">{daily_queries_based_on_your_budget:.0f} queries per day</span> when using <span style="color: rgb(255, 75, 75);">{model_choice}</span>.</p>', unsafe_allow_html=True)
        st.write("Based on 250 working days and Prompt + Input + Output.")


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

    st.markdown(f'<p style="text-align:center; font-weight: bold;"><span style="color: rgb(255, 75, 75); font-size: 24px">${minNewTotal:.2f} - ${maxNewTotal:.2f}</span></p>', unsafe_allow_html=True)
    st.write(f'<p style="text-align:center;">are the costs for <span style="color: rgb(255, 75, 75)"> {values[0]} - {values[1]}</span> queries when using <span style="color: rgb(255, 75, 75);">{model_choice}.</span></p>', unsafe_allow_html=True)

    st.divider()
    st.header("Freely adjust Tokens")
    st.write("The idea of this section is to give you the option to freely adjust the amount of Prompt, Input and Output Tokens. It is divided in min and max eacht time to give you the option to enter the minimum of Tokens you think you need and the maximum amount of Tokens you expect to need. The results will display the cost for 1 query (min and max cost) as well as for your query range you set up above.")
    col5, col6, col7 = st.columns(3)
    col51, col52, col61, col62, col71, col72 = st.columns(6)

    with col5: 
        st.subheader("Vary the Prompt Tokens.")
        with col51:
            min_number_prompt = st.number_input('Insert min Prompt Tokens', value=50)
            min_single_result_prompt = min_number_prompt * modelInputCost / 1000
            min_multiple_result_prompt = min_number_prompt * modelInputCost / 1000 * values[0]
            st.markdown(f'<p><span style="color: rgb(255, 75, 75);">{min_number_prompt:.0f} Prompt Tokens</span> would cost for 1 query <span style="color: rgb(255, 75, 75);">{min_single_result_prompt:.7f}$ </span> and <span style="color: rgb(255, 75, 75);">{min_multiple_result_prompt:.2f}$</span> for <span style="color: rgb(255, 75, 75);">{values[0]} queries</span>.</p>', unsafe_allow_html=True)
        with col52:
            max_number_prompt = st.number_input('Insert max Prompt Tokens', value=150)
            max_single_result_prompt = max_number_prompt * modelInputCost / 1000
            max_multiple_result_prompt = max_number_prompt * modelInputCost / 1000 * values[1]
            st.markdown(f'<p><span style="color: rgb(255, 75, 75);">{max_number_prompt:.0f} Prompt Tokens</span> would cost for 1 query <span style="color: rgb(255, 75, 75);">{max_single_result_prompt:.7f}$ </span> and <span style="color: rgb(255, 75, 75);">{max_multiple_result_prompt:.2f}$</span> for <span style="color: rgb(255, 75, 75);">{values[1]} queries</span>.</p>', unsafe_allow_html=True)

    with col6:
        st.subheader("Vary the Input Tokens.")
        with col61:
            min_number_input = st.number_input('Insert min Input Tokens', value=400)
            min_single_result_input = min_number_input * modelInputCost / 1000
            min_multiple_result_input = min_number_input * modelInputCost / 1000 * values[0]
            st.markdown(f'<p><span style="color: rgb(255, 75, 75);">{min_number_input:.0f} Prompt Tokens</span> would cost for 1 query <span style="color: rgb(255, 75, 75);">{min_single_result_input:.7f}$ </span> and <span style="color: rgb(255, 75, 75);">{min_multiple_result_input:.2f}$</span> for <span style="color: rgb(255, 75, 75);">{values[0]} queries</span>.</p>', unsafe_allow_html=True)
        with col62:
            max_number_input = st.number_input('Insert max Input Tokens', value=800)
            max_single_result_input = max_number_input * modelInputCost / 1000
            max_multiple_result_input = max_number_input * modelInputCost / 1000 * values[1]
            st.markdown(f'<p><span style="color: rgb(255, 75, 75);">{max_number_input:.0f} Prompt Tokens</span> would cost for 1 query <span style="color: rgb(255, 75, 75);">{max_single_result_input:.7f}$ </span> and <span style="color: rgb(255, 75, 75);">{max_multiple_result_input:.2f}$</span> for <span style="color: rgb(255, 75, 75);">{values[1]} queries</span>.</p>', unsafe_allow_html=True)
    
        
    with col7:
        st.subheader("Vary the Output Tokens.")
        with col71:
            min_number_output = st.number_input('Insert min Output Tokens', value=50)
            min_single_result_output = min_number_output * modelOutputCost / 1000
            min_multiple_result_output = min_number_output * modelOutputCost / 1000 * values[0]
            st.markdown(f'<p><span style="color: rgb(255, 75, 75);">{min_number_output:.0f} Prompt Tokens</span> would cost for 1 query <span style="color: rgb(255, 75, 75);">{min_single_result_output:.7f}$ </span> and <span style="color: rgb(255, 75, 75);">{min_multiple_result_output:.2f}$</span> for <span style="color: rgb(255, 75, 75);">{values[0]} queries</span>.</p>', unsafe_allow_html=True)
    
        with col72:
            max_number_output = st.number_input('Insert max Output Tokens', value=150)
            max_single_result_output = max_number_output * modelOutputCost / 1000
            max_multiple_result_output = max_number_output * modelOutputCost / 1000 * values[1]
            st.markdown(f'<p><span style="color: rgb(255, 75, 75);">{max_number_output:.0f} Prompt Tokens</span> would cost for 1 query <span style="color: rgb(255, 75, 75);">{max_single_result_output:.7f}$ </span> and <span style="color: rgb(255, 75, 75);">{max_multiple_result_output:.2f}$</span> for <span style="color: rgb(255, 75, 75);">{values[1]} queries</span>.</p>', unsafe_allow_html=True)
    #calcs
    min_total_result = min_single_result_prompt + min_single_result_input + min_single_result_output
    max_total_result = max_single_result_prompt + max_single_result_input + max_single_result_output

    min_multiple_total_result = min_multiple_result_prompt + min_multiple_result_input + min_multiple_result_output
    max_multiple_total_result = max_multiple_result_prompt + max_multiple_result_input + max_multiple_result_output

    min_tokens_num = min_number_prompt + min_number_input + min_number_output
    max_tokens_num = max_number_prompt + max_number_input + max_number_output

    min_prompt_input_prozent = ((min_number_prompt+min_number_input) * modelInputCost / 1000 ) / (min_tokens_num * modelInputCost / 1000) * 100
    min_output_prozent = ((min_number_output) * modelOutputCost / 1000 ) / (min_tokens_num * modelOutputCost / 1000) * 100

    max_prompt_input_prozent = ((max_number_prompt+max_number_input) * modelInputCost / 1000 ) / (max_tokens_num * modelInputCost / 1000) * 100
    max_output_prozent = ((max_number_output) * modelOutputCost / 1000 ) / (max_tokens_num * modelOutputCost / 1000) * 100

    st.markdown(f'<p style="text-align:center; font-weight: bold;"><span style="color: rgb(255, 75, 75); font-size: 24px">${min_total_result:.7f} - ${max_total_result:.7f}</span></p>', unsafe_allow_html=True)
    st.write(f'<p style="text-align:center;">are the min & max costs for 1 query based on min <span style="color: rgb(255, 75, 75);">{min_tokens_num}</span> total tokens ({min_number_prompt}+{min_number_input}+{min_number_output}) with the following cost distribution in percent for the Input (Prompt + Input): <span style="color: rgb(255, 75, 75);">{min_prompt_input_prozent:.2f}%</span> and for Output: <span style="color: rgb(255, 75, 75);">{min_output_prozent:.2f}%</span> and max <span style="color: rgb(255, 75, 75);">{max_tokens_num}</span> total tokens ({max_number_prompt}+{max_number_input}+{max_number_output}) with the following cost distribution in percent for the Input (Prompt + Input): <span style="color: rgb(255, 75, 75);">{max_prompt_input_prozent:.2f}%</span> and for Output: <span style="color: rgb(255, 75, 75);">{max_output_prozent:.2f}%</span> when using <span style="color: rgb(255, 75, 75);">{model_choice}.</span></p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; font-weight: bold;"><span style="color: rgb(255, 75, 75); font-size: 24px">${min_multiple_total_result:.2f} - ${max_multiple_total_result:.2f}</span></p>', unsafe_allow_html=True)
    st.write(f'<p style="text-align:center;">are the costs for <span style="color: rgb(255, 75, 75)"> {values[0]} - {values[1]}</span> queries based on your settings when using <span style="color: rgb(255, 75, 75);">{model_choice}.</span></p>', unsafe_allow_html=True)
    
