from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Initialize the language model (Make sure to set your OpenAI API key)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

def generate_cheer_response(log, tone="happy"):
    template = """
    User Exercise Log: {log}
    Tone: {tone}
    Generate a cheer response in the given tone.
    
    Examples:
    User Exercise Log: "I ran 5km today."
    Tone: "happy"
    Response: "Amazing job! You're pushing your limits and getting stronger every day! Keep it up!"
    
    User Exercise Log: "I lifted weights for 30 minutes."
    Tone: "angry"
    Response: "Finally! About time you showed some real effort. No excuses, keep going!"
    
    User Exercise Log: {log}
    Tone: {tone}
    Response:
    """
    prompt = PromptTemplate.from_template(template)
    response = llm.predict(prompt.format(log=log, tone=tone))
    return response

# Example inputs and outputs
exercise_log = "I ran 2km today."

# Happy Response
happy_cheer = generate_cheer_response(exercise_log, tone="happy")
print("Happy Response:", happy_cheer)

# Angry Response
angry_cheer = generate_cheer_response(exercise_log, tone="angry")
print("Angry Response:", angry_cheer)

if __name__ == "__main__":
    tone = "happy"
    user_input = 'I run 2km today'

    response = generate_cheer_response(user_input, tone)
    print(response)
