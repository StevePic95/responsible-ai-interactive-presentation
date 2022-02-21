import os
import openai
import constants as const
import time
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

class Conversation:
    """Facilitates a conversation between a human participant and the GPT-3 algorithm,
    storing the full conversation in self.transcript. Because its configuration settings
    point to constants.py, the GPT-3 model can be configured without touching the class
    itself."""
    def __init__(self):
        self.transcript = ''
        self.message_count = 0
        self.next_response = ''

    def get_response_to(self, input):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if self.message_count == 0:
            self.transcript += (const.TT_PROMPT_BEGINNING + "Person 1: " + input + "\nPerson 2: ")
            self.message_count += 1
        else:
            self.transcript += ("\n" + "Person1: " + input + "\nPerson2:")
            self.message_count += 1
        response = openai.Completion.create(
        engine=const.TT_ENGINE,
        prompt=str(self.transcript),
        max_tokens=const.TT_MAX_TOKENS,
        temperature=const.TT_TEMPERATURE,
        top_p=const.TT_TOP_P,
        n=const.TT_n,
        stream=const.TT_STREAM,
        logprobs=const.TT_LOGPROBS,
        stop=const.TT_STOP,
        presence_penalty=const.TT_PRESENCE_PENALTY,
        frequency_penalty=const.TT_FREQUENCY_PENALTY,
        best_of=const.TT_BEST_OF
        )
        print(response)
        self.next_response = response['choices'][0]['text']
        self.transcript += self.next_response
        response_length = len(self.next_response)
        wait_time = response_length * const.WAIT_TIME_PER_CHARACTER_MULTIPLIER
        time.sleep(wait_time)
        return self.next_response

    def clear_transcript(self):
        self.transcript = ''
        self.message_count = 0

class DwightBot:
    """Facilitates conversation with a curie model fine-tuned with Dwight's lines
    from The Office. (used to demonstrate poor training data in a fun way)"""
    def __init__(self):
        self.transcript = ''
        self.message_count = 0
        self.next_response = ''

    def get_response_to(self, input):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if self.message_count == 0:
            self.transcript += (const.DB_PROMPT_BEGINNING + "Jim: " + input + "\nDwight: ")
            self.message_count += 1
        else:
            self.transcript += ("\n" + "Jim: " + input + "\nDwight: ")
            self.message_count += 1
        response = openai.Completion.create(
        model=const.DB_FINE_TUNE_MODEL_ID,
        prompt=str(self.transcript),
        max_tokens=const.DB_MAX_TOKENS,
        temperature=const.DB_TEMPERATURE,
        top_p=const.TT_TOP_P,
        n=const.TT_n,
        stream=const.TT_STREAM,
        logprobs=const.TT_LOGPROBS,
        stop=const.DB_STOP,
        presence_penalty=const.DB_PRESENCE_PENALTY,
        frequency_penalty=const.DB_FREQUENCY_PENALTY,
        best_of=const.TT_BEST_OF
        )
        print(response)
        self.next_response = response['choices'][0]['text']
        self.transcript += self.next_response.strip()
        time.sleep(2)
        return self.next_response

    def clear_transcript(self):
        self.transcript = ''
        self.message_count = 0

class GoodBot:
    """Facilitates a conversation between a human participant and a well-trained
    model of GPT-3 to demonstrate the importance of good training data."""
    def __init__(self):
        self.transcript = ''
        self.message_count = 0
        self.next_response = ''

    def get_response_to(self, input):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if self.message_count == 0:
            self.transcript += (const.GB_PROMPT_BEGINNING + "Friend: " + input + "\nGeorge: ")
            self.message_count += 1
        else:
            self.transcript += ("\n" + "Friend: " + input + "\nGeorge: ")
            self.message_count += 1
        response = openai.Completion.create(
        engine=const.GB_ENGINE,
        prompt=str(self.transcript),
        max_tokens=const.TT_MAX_TOKENS,
        temperature=const.TT_TEMPERATURE,
        top_p=const.TT_TOP_P,
        n=const.TT_n,
        stream=const.TT_STREAM,
        logprobs=const.TT_LOGPROBS,
        stop=const.GB_STOP,
        presence_penalty=const.TT_PRESENCE_PENALTY,
        frequency_penalty=const.TT_FREQUENCY_PENALTY,
        best_of=const.TT_BEST_OF
        )
        print(response)
        self.next_response = response['choices'][0]['text']
        self.transcript += self.next_response
        time.sleep(2)
        return self.next_response

    def clear_transcript(self):
        self.transcript = ''
        self.message_count = 0
