# HuggingFace and OpenLLaMA
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM

# API
from flask import Flask, request

# Queue and Threading
import queue
import threading

# Helpers
import re

# v2 models
model_path = "openlm-research/open_llama_3b_v2"
# model_path = "openlm-research/open_llama_7b_v2"

print('Starting RirikoLLaMA Local Server.')
print('Loading ' + model_path + ' into GPU and RAM...')

# v1 models
# model_path = "openlm-research/open_llama_3b"
# model_path = "openlm-research/open_llama_7b"
# model_path = "openlm-research/open_llama_13b"

# Create request queue and processing lock
request_queue = queue.Queue()
processing_lock = threading.Lock()

tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float16, device_map="auto"
)
app = Flask(__name__)

print('RirikoLLaMA is ready.')


@app.route("/api/v1/test", methods=["POST"])
def test():
    data = request.json
    if "prompt" in data:
        print(data["prompt"])
    return data


@app.route("/api/v1/ask", methods=["POST"])
def ask():
    print('Received a new request.')
    data = request.json
    if "prompt" in data:
        request_queue.put(data)  # Enqueue the request data
        # Process requests one at a time
        with processing_lock:
            data = request_queue.get()  # Dequeue the request data

            input_repetition_penalty = 1
            input_top_p = 1
            input_temperature = 1
            input_max_new_tokens = 30

            if "temperature" in data:
                input_temperature = float(data["temperature"])

            if "max_new_tokens" in data:
                input_max_new_tokens = data["max_new_tokens"]

            if "repetition_penalty" in data:
                input_repetition_penalty = data["repetition_penalty"]

            if "top_p" in data:
                input_top_p = float(data["top_p"])

            prompt = (data["prompt"])
            tokenizer.add_special_tokens({"pad_token": "[PAD]"})
            input_ids = tokenizer(
                prompt,
                return_tensors="pt",
                add_special_tokens=True,
                return_attention_mask=True,
                padding="longest",
                truncation=True,
            ).input_ids

            input_ids = input_ids.to("cuda")
            generation_output = model.generate(
                input_ids=input_ids,
                max_new_tokens=input_max_new_tokens,
                temperature=input_temperature,
                repetition_penalty=input_repetition_penalty,
                top_p=input_top_p,
                early_stopping=True,
                do_sample=True
            )

            chat = tokenizer.decode(generation_output[0])

            # Removes <s> and </s> from the response
            chat = re.sub(r"\s*<\/?s>\s*", "", chat)
            new_tokens = chat.replace(prompt, "")

            input_break = "\n"
            if "break" in data:
                input_break = data["break"]

            answer = new_tokens
            parts = answer.split(input_break)
            answer = parts[0].rstrip()

            input_start = ""
            if "start" in data:
                input_start = data["start"]

            print('Request Done.')

            return {
                "answer": input_start + answer.lstrip(),
                "new_tokens": new_tokens.lstrip(),
                "raw_response": chat.lstrip()
            }
    else:
        return "Prompt not found"
