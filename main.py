# Audio / Audio processing libraries
import pyaudio
import numpy as np

# System libraries
import os
from dotenv import load_dotenv
import concurrent.futures

# Communication libraries
from twilio.rest import Client
import smtplib

# These are some global variables that we're going to use to both
# read the audio from the microphone and normalize it.
#
# It might be a good idea to put this on a config or .env file
SAMPLES = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SILENCE_THRESHOLD = 20

# This constant is the constant that will determin if we should
# notify the user or not. According to studies, a human scream
# ranges from 80 to 110 dB, and we don't want false positives
DANGER_LEVEL = 85

load_dotenv()

twilio_sid = os.getenv("TWILIO_SID")
twilio_token = os.getenv("TWILIO_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")

try:
    twilio_client = Client(twilio_sid, twilio_token)
except Exception:
    print("There was an error creating the Twilio client")
    exit(1)


def main():
    capture_audio()


# This function takes care of recording the audio from the
# microphone to be processed later on
def capture_audio():
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=SAMPLES
    )

    print("Listening...")

    try:
        while True:
            calculate_decibels(stream)
    except KeyboardInterrupt:
        print("\nStopping...\n")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


# This function takes care of getting the stream as an input,
# read the data from it and then calculate the decibels
def calculate_decibels(stream):
    data = np.frombuffer(stream.read(SAMPLES), dtype=np.int16)

    # RMS stands for "root mean square". Some fancy math sh*t
    rms = np.sqrt(np.mean(data ** 2))

    # This will convert from RMS to decibels, measured in dB
    decibels = 20 * np.log10(rms) if rms > 0 else -np.inf

    if decibels != -np.inf and decibels > SILENCE_THRESHOLD:
        print(f"Raw RMS: {rms}, Decibels: {decibels:.2f}")

    if decibels >= DANGER_LEVEL:
        trigger_emergency()


# ALL HANDS ON DECK, THIS IS NOT A DRILL
# If this function is triggered, then this means that
# something really bad happened and we're now
# starting the emergency protocol
def trigger_emergency():
    numbers = parse_numbers()
    emails = parse_emails()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        sms_future = executor.submit(send_sms, numbers)
        emails_future = executor.submit(send_emails, emails)

        concurrent.futures.wait([sms_future, emails_future])


# This function takes care of looping through all the trusted numbers
# and sending them the message in case of emergency
def send_sms(numbers):
    message = os.getenv("MESSAGE")

    for number in numbers:
        try:
            twilio_message = twilio_client.messages.create(
                to=number,
                from_=twilio_number,
                body=message
            )
            print(
                f"Message with SID {twilio_message.sid} sent to {number}"
            )
        except Exception:
            print("Error sending message")


# Much like the send_sms() function, this one takes care of sending
# emails to the trusted emails on the list, present in the
# .env file
def send_emails(emails):
    message = os.getenv("MESSAGE")

    # Load all the SMTP variables
    server = os.getenv("SMTP_SERVER")
    port = os.getenv("SMTP_PORT")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")

    from_address = os.getenv("SMTP_EMAIL")

    try:
        with smtplib.SMTP(server, port) as server:
            server.starttls()
            server.set_debuglevel(1)

            try:
                server.login(username, password)
            except smtplib.SMTPAuthenticationError as auth_error:
                print(f"Authentication Failed: {auth_error}")
                return

            for email in emails:
                print(email)

                try:
                    server.sendmail(from_address, email, message)
                    print(f"Email sent to {email}")
                except Exception as e:
                    print(repr(e))
    except Exception as connection_error:
        print(f"SMTP connection error: {connection_error}")


# In our .env file we'll have a list of trusted numbers that get contacted
# when there's an emergency, separated by "," and we want to get each
# one individually to be contacted
def parse_numbers():
    trusted_numbers = os.getenv("TRUSTED_NUMBERS").replace(" ", "")

    return trusted_numbers.split(",")


# You know the drill here.
def parse_emails():
    trusted_emails = os.getenv("TRUSTED_EMAILS").replace(" ", "")

    return trusted_emails.split(",")


if __name__ == "__main__":
    main()
