from flask import Flask, request, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse
import time
import os
from twilio.rest import Client

from utils import fetch_reply
import dialogflow 
from paynow import Paynow

app = Flask(__name__)

GOOD_BOY_URL = (
    "https://scontent.fhre1-1.fna.fbcdn.net/v/t1.6435-9/235465023_2764744417155942_3504578660793433865_n.jpg?_nc_cat=104&ccb=1-5&_nc_sid=730e14&_nc_ohc=LoKDEglDbPAAX-f_vCy&_nc_ht=scontent.fhre1-1.fna&oh=0af85433a74c8852012a4f8455212d77&oe=6146125B"
    "&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    phone_no = request.form.get('From')
    reply = fetch_reply(msg, phone_no)

    # Create reply
    resp = MessagingResponse()
    resp.message(reply)

    return str(resp)

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():
    try:
        my_input = request.form.get('Body')
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not my_input:
        msg = response.message("Send valid input!")
        
    else:
        msg = response.message("*The diagram above shows a velocity-time graph for a moving object* \n\n Calculate \n\na) The acceleration during the first 6 seconds \n\nb) The total distance travelled by the object \n\nc) The velocity when _t_ = 13s")
        msg.media(GOOD_BOY_URL)
    return str(response)


@app.route("/paynow")
def my_form():
    return render_template('index.html')

@app.route("/paynow", methods=['POST','GET'])
def paynow():
    paynow = Paynow(
        '12455', 
        '79d50d72-278f-48ac-83c7-cf4e5dfb5615',
        'https://gonai.rg.gd/register.html', 
        'https://www.google.com'
        )

    payment = paynow.create_payment('Gonai Subscription', 'krchikwangwani@gmail.com')

    payment.add('Payment for Qray Gonai subscription', 350)

    text = request.form['text']

    response = paynow.send_mobile(payment, text, 'ecocash')


    if(response.success):
       
        poll_url = response.poll_url

        print("Poll Url: ", poll_url)

        status = paynow.check_transaction_status(poll_url)

        time.sleep(30)

        print("Payment Status: ", status.status)

    status = paynow.check_transaction_status(poll_url)
    return redirect(response.redirect_url)

@app.route("/register",methods=['POST', 'GET'])
def reg_form():
    return render_template('register.html')
  
if __name__ == "__main__":
    app.run(debug=True)