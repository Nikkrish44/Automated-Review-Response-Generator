from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Initialize Ollama chat model 
chat = ChatOllama(model="llama3", max_tokens=150, temperature=0.5)  

#sentiment analysis
def analyze_sentiment(review):
    try:
        prompt = f"Analyze the sentiment of the following customer review (positive, neutral, or negative): {review}"
        response = chat.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:  
        print(f"Error in sentiment analysis: {e}")
        return None

#theme extraction
def extract_themes(review):
    try:
        prompt = f"Identify the key themes from the following customer review: {review}"
        response = chat.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        print(f"Error in theme extraction: {e}")
        return None


def generate_response(review, name, companyname, repname):
    sentiment = analyze_sentiment(review)
    themes = extract_themes(review)
    
    # print(f"Sentiment: {sentiment}")
    # print(f"Themes: {themes}")
    if sentiment is None or themes is None:
        return "Error: Unable to analyze the review."
    
    try:
        prompt = f"""Write a professional email response to a customer based on the following review, sentiment, and key themes: 
        Review: "{review}"
        Sentiment: {sentiment}
        Key Themes: {themes}
        
        Start the email with: 'Dear {name},' use company name: {companyname}, my name as {repname}, and maintain a polite, professional tone. 
        **Do not use any brackets [] in the email. Do not start with "Here is a professional email response to the customer:" or similar phrases.
        Be concise and don't be repetitive, **no more than 150 words**.
        """        
        response = chat.invoke([HumanMessage(content=prompt)])


        return response.content.strip()
    except Exception as e:
        print(f"Error in generating response: {e}")
        return None

def returncoloredresponse(response):
    green_color = "\033[32m"  # Green text 
    reset = "\033[0m"  # Reset to default 
    bolded_text = "\033[1m"  # Bold text
    col_response = f"{green_color}{bolded_text}{response}{reset}"
    return col_response

def send_email(sender_email, sender_password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  
        server.login(sender_email, sender_password)  
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send
        server.quit()  # Close
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    


# Example usage
customername = "Nick"  
representative_name = "Mike Waz"  
company_name = "Purvis Industries"

customer_review1 = """I am really disappointed with the shipping time. It took way longer than expected, and there were no clear updates on the delivery status. On top of that, when I reached out to customer service for help, they were unresponsive and not helpful at all. I expected better communication and service. Definitely not a great experience.""" 

customer_review2 = """The product works as described, but I found the setup process quite complicated. It took me a while to get everything running, and the instructions weren’t very clear. I think a more detailed guide or better support resources would be helpful. Other than that, the product itself seems decent."""

customer_review3 = """I just wanted to say how impressed I am with my purchase! 
The quality exceeded my expectations, and the shipping was super fast. 
I also had a small question about usage, and your support team responded quickly and was very helpful. Keep up the great work!"""

response_email = generate_response(customer_review1, customername, company_name, representative_name)
print(returncoloredresponse(response_email))

send_email("wazmike417@gmail.com", "**REDACTED**", "**REDACTED**", "RE: Your Product Review", response_email)

