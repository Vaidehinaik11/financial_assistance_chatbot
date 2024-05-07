import openai
import streamlit as st
import json

openai.api_key = open('API_KEY', 'r').read()

def risk_analysis(gender, age, income, savings, monthly_expenses, debt, credit_score, investment):
    age = int(age)
    income = int(income)
    savings = int(savings)
    monthly_expenses = int(monthly_expenses)
    # debt = int(debt)
    credit_score = int(credit_score)
    # investment = int(investment)

    # Calculate the financial risk score
    risk_score = 0
    
    # Adjust risk score based on gender, age, and credit score
    if gender.lower() == "male":
        risk_score += 5
    elif gender.lower() == "female":
        risk_score += 3
    else:
        risk_score += 4
    
    if age < 30:
        risk_score -= 3
    elif 30 <= age <= 50:
        risk_score += 2
    else:
        risk_score += 5
    
    if 300 <= credit_score < 580:
        risk_score += 10
    elif 580 <= credit_score < 670:
        risk_score += 8
    elif 670 <= credit_score < 740:
        risk_score += 5
    elif 740 <= credit_score < 800:
        risk_score += 3
    elif 800 <= credit_score:
        risk_score -= 2
    
    # Adjust risk score based on savings, monthly expenses, debt, and investment
    if savings < monthly_expenses * 3:
        risk_score += 10
    elif savings < monthly_expenses * 6:
        risk_score += 5
    elif savings < monthly_expenses * 12:
        risk_score += 2
    else:
        risk_score -= 3
    
    # if debt > income * 0.5:
    #     risk_score += 10
    # elif debt > income * 0.3:
    #     risk_score += 5
    # elif debt > income * 0.1:
    #     risk_score += 2
    # else:
    #     risk_score -= 3
    
    # if investment < income * 0.2:
    #     risk_score += 10
    # elif investment < income * 0.4:
    #     risk_score += 5
    # elif investment < income * 0.6:
    #     risk_score += 2
    # else:
    #     risk_score -= 3
    
    
    # Determine personality based on risk score
    if 0 <= risk_score <= 10:
        personality = "Conservative Investor"
    elif 11 <= risk_score <= 20:
        personality = "Moderate Investor"
    else:
        personality = "Aggressive Investor"
    
    return personality

function_descriptions = [
    {
        "name": "risk_analysis",
        "description": "This function performs personal financial risk analysis, including the interpretation of gender, age, expenses, income, future investment plans, risk-taking aspects, and outputs the person's financial personality.",
        "parameters": {
            "type": "object",
            "properties": {
                "gender": {
                    "type": "string",
                    "description": "The gender of the individual (e.g., 'male', 'female', 'non-binary').",
                },
                "age": {
                    "type": "string",
                    "description": "The age of the individual.",
                },
                "income": {
                    "type": "string",
                    "description": "The annual income of the individual.",
                },
                "savings": {
                    "type": "string",
                    "description": "The amount of savings the individual has.",
                },
                "monthly_expenses": {
                    "type": "string",
                    "description": "The total monthly expenses of the individual.",
                },
                "debt": {
                    "type": "string",
                    "description": "The total amount of debt the individual has.",
                },
                "credit_score": {
                    "type": "string",
                    "description": "The credit score of the individual.",
                },
                "investment": {
                    "type": "string",
                    "description": "The total investment amount of the individual.",
                }
            },
            "required": ["gender", "age", "income", "savings", "monthly_expenses", "debt", "credit_score", "investment"]
        }
    }
]


available_function = {
    'risk_analysis': risk_analysis
}


if 'messages' not in st.session_state:
    st.session_state['messages'] = [] 

st.title("financial assistant chatbot")

st.session_state['messages'].append({"role":"system", "content":"You are a financial experts that specializes in analysing individual financial behaviour and advising on investment"})

user_input = st.text_input("your_input:")

if user_input:
    try:
        st.session_state['messages'].append({"role":"user", "content": f"{user_input}"})
        
        response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = st.session_state['messages'],
                functions = function_descriptions,
                function_call = "auto"
            )
        response_message = response.choices[0].message
        
        if response_message.get('function_call'):
            funct_name = response_message['function_call']['name']
            funct_args = json.loads(response_message['function_call']['arguments'])
            if funct_name in ['risk_analysis']:
                args_dict = {'gender':funct_args.get('gender'), 'age':funct_args.get('age'), 'income':funct_args.get('income'), 'savings':funct_args.get('savings'), 'monthly_expenses':funct_args.get('monthly_expenses'), 'debt':funct_args.get('debt'), 'credit_score':funct_args.get('credit_score'), 'investment':funct_args.get('investment')
                
                }

            funt_to_call = available_function[funct_name]
            funt_resp = funt_to_call(**args_dict)

            st.session_state['messages'].append(response_message)
            st.session_state['messages'].append({'role': 'function','name': funct_name, 'content':funt_resp})

            second_response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = st.session_state['messages'])
            
            st.text(second_response.choices[0].message['content'])
            st.session_state['messages'].append({'role':'assistant', 'content': second_response.choices[0].message['content']})
        else:
            st.text(response_message['content'])
            st.session_state['messages'].append({'role':'assistant', 'content': response_message['content']})
    except Exception as e:        
        raise e

