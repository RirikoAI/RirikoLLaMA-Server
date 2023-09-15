# RirikoLLaMA Server
Introducing Ririko LLaMA, now you can run your own "ChatGPT" at home! (With OpenLLaMA, 100% FOC).

| !! Note: This is just the LLaMA RESTful server. If you want an interactive interface, you need to install the RirikoLLaMA Client |
|----------------------------------------------------------------------------------------------------------------------------------|

## To run the server in your computer
To run the `open_llama_3b_v2` (3 billion parameters) model, you will need:
1) For CPU only inference: At least 16GB of RAM
2) For GPU + CPU inference: At least 5GB of GPU vRAM + 10GB of RAM
3) GPU only inference: At least 12GB of GPU vRAM

Inferencing speed: Speed varies depending on your GPU and RAM speed. I'm running the server with
Ryzen 9 5900X, 32GB of RAM and an RTX 2060 (using GPU + CPU approach), and I'm generating about 
3 new tokens per second.

### 1. Install Python 3.11 in your PC:
https://www.python.org/downloads/release/python-3110/ (Install it to C:\Python311)

### 2. Install pip
- Download this file https://bootstrap.pypa.io/get-pip.py (Download this to C:\Python311 or the 
same directory where your Python installation is)
- Open your terminal (Command Prompt / PowerShell)
- Change dir to the Python installation folder: `cd C:\Python311`
- Install pip: `python get-pip.py`
- Check if pip is successfully installed: `pip --version`

### 3. Activate virtual environment
```python3 -m venv venv```

### 4. Install requirements
```pip install -r requirements.txt```

### 5. Run the LLaMA server
```flask run```

The server will now run locally at:  http://127.0.0.1:5000.
You can send a POST request to `http://localhost:5000/api/v1/ask` API endpoint for your chatbot.

## Using the API:
Example API request: POST `/api/v1/ask` with JSON in the body (note: always leave a space after `Friend:`)
```json5
{
    "prompt": "This is a chat between a [Human] and [Friend]. The [Friend] is very nice and empathetic. The [Friend] name is Ririko. [Friend] Loves to talk about anime, manga & science.\n\nHuman: Hi Ririko! I'm Angel.\nFriend: Hi, Angel.\nHuman: Tell me about yourself.\nFriend: ",
    "max_new_tokens": 30,
    "temperature": 3.0,
    "repetition_penalty": 1,
    "top_p": 0.2,
    "start": "Friend: ",
    "break": "\n"
}
```

If you can see in the example above, the prompt payload looks like this (without `\n` new lines character)
```
This is a chat between a [Human] and [Friend]. The [Friend] is very nice and empathetic. 
The [Friend] name is Ririko. [Friend] Loves to talk about anime, manga & science.

Human: Hi Ririko! I'm Angel.
Friend: Hi, Angel.
Human: Tell me about yourself.
Friend: 
```

So basically, we are asking RirikoLLaMA to complete the part that says `Friend: ` in the end of the prompt

### Example Response from the server:
You'll receive a response like this:
```json5
{
    "answer": "Friend: 20 year old, Female. Loves to talk about anime, manga & science.",
    "new_tokens": "20 year old, Female. Loves to talk about anime, manga & science.\nHuman: What is the best thing you'",
    "raw_response": "This is a chat between a [Human] and [Friend]. The [Friend] is very nice and empathetic. The [Friend] name is Ririko. [Friend] Loves to talk about anime, manga & science.\n\nHuman: Hi Ririko! I'm Angel.\nFriend: Hi, Angel.\nHuman: Tell me about yourself.\nFriend: 20 year old, Female. Loves to talk about anime, manga & science.\nHuman: What is the best thing you'"
}
```
So, you will keep appending the `answer` into your prompt and ask it to generate new responses
and essentially having a "conversation".