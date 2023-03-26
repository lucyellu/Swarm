import anthropic
import openai
import os
import random

def round_robin_storytelling(api_key, openai_key, story_so_far, model="claude-v1"):
    while True:
        next_token_anthropic = get_next_token_anthropic(api_key, story_so_far, model)
        story_so_far += next_token_anthropic

        next_token_openai = get_next_token_openai(openai_key, story_so_far)
        story_so_far += next_token_openai

        print(story_so_far)

def get_next_token_anthropic(api_key, story_so_far, model="claude-v1"):
    client = anthropic.Client(api_key)

    #prompt = f"{anthropic.HUMAN_PROMPT} Round-robin storytelling game:\n\nStory so far: {story_so_far}\n\n{anthropic.AI_PROMPT}Next token:"
    prompt = f"{anthropic.HUMAN_PROMPT} You are participating in a round-robin storytelling game, where each player contributes one sentance a time to create a coherent and grammatically correct story. Your task is to add the next sentance, ensuring that the whole remains both grammatically and syntactically accurate. Only output a single next sentance, do not include any additional information. Please include spaces as approprate at the beginning of the sentance. The story so far is: {story_so_far}{anthropic.AI_PROMPT}"

    response = client.completion(
        prompt=prompt,
        model=model,
        max_tokens_to_sample=20,
        stop_sequences=["."]
    )

    next_token = response['completion']
    return next_token

def get_next_token_openai(openai_key, story_so_far):
    openai.api_key = openai_key

    #messages = [
    #    {"role": "user", "content": f"Round-robin storytelling game:\n\nStory so far: {story_so_far}\n\nNext token:"}
    #]
    messages = [
        {"role": "user", "content": f"You are participating in a round-robin storytelling game, where each player contributes one sentance a time to create a coherent and grammatically correct story. Your task is to add the next sentance, ensuring that the whole remains both grammatically and syntactically accurate. Only output a single next sentance, do not include any additional information. Please include spaces as approprate at the beginning of the sentance. The story so far is: {story_so_far}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=20
    )

    next_token = response['choices'][0]['message']['content']
    return next_token

def main():
    anthropic_api_key = os.environ["ANTHROPIC_API_KEY"]
    openai_api_key = os.environ["OPENAI_API_KEY"]
    story_intros = [
    "Once upon a time, in a land far, far away, a young boy embarked on an epic journey. ",
    "It was the best of ",
    "Four score and ",
    "Far out in the uncharted backwaters ",
    "I'm pretty much f*cked. ",
    "It was a pleasure to burn. ",
    "It was the day my ",
    "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be ",
    "Mr. and Mrs. Dursley of number four, Privet Drive, ",
    "It was the best of times, it was ",
    "All children, except one, ",
    "All this happened, more or less. ",
    "The story so far: ",
    "If you really want to hear about it, the first thing you'll probably ",
    "Alice was beginning to get very tired of sitting by her sister on the bank and of having nothing to do: once ",
    "A long time ago in a galaxy far, far away, "
    ]
    story_so_far=random.choice(story_intros)
    round_robin_storytelling(anthropic_api_key, openai_api_key, story_so_far)

if __name__ == "__main__":
    main()
