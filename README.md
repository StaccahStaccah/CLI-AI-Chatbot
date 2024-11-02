

# Gemini Chatbot CLI

This is a Command Line Interface (CLI) chatbot that uses the Gemini SDK by Google for natural language generation. The chatbot allows users to interactively ask questions and receive responses, using the configured model.

## ✨ Features

- Interactive command line interface for chatting.
- Configurable model parameters using a JSON file (`config.json`), allowing adjustments for:
  - **Temperature**: Controls the creativity of the model's responses.
  - **Max Tokens**: Sets the maximum number of tokens in the response.
  - **Top-K Sampling**: Limits sampling to the top K most probable tokens.
  - **Top-P Sampling**: Uses cumulative probability to determine which tokens to include.
- Visual elements such as ASCII art and colored messages using the `rich` library for better terminal experience.

## 📋 Prerequisites

- Python 3.8+
- Google Gemini SDK (`google.generativeai`)
- Rich (`rich`) for better terminal visualization
- Dotenv (`python-dotenv`) for managing environment variables
- Gemini API Key ([Get your API Key here](https://developers.generativeai.google.com/docs/get-api-key))
  
  
## ⚙️ Installation

1. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root directory of the project and add your Gemini API key and model name:

> model name list:
>
> - gemini-1.5-flash
> - gemini-1.5-pro
> - gemini-1.0-pro
> - text-embedding-004
> - aqa

   ```env
   API_KEY=your_gemini_api_key
   MODEL_NAME=your_model_name
   ```

3. Edit `config.json` file to adjust the model configuration:

   ```json
   {
     "temperature": 0.7,
     "max_tokens": 200,
     "top_k": 40,
     "top_p": 0.9
   }
   ```

## 🚀 Usage

Run the chatbot by executing the following command:

```sh
python run.py
```

You will see an ASCII art banner and be prompted to start chatting.

- Type your messages and press enter to receive a response.
- To exit the chat, type `!exit`.

## 🔧 How to Configure

You can modify the behavior of the model by changing the values in `config.json`:

- **temperature**: Controls how creative the response is. A value closer to 1.0 results in more creative responses, while a value closer to 0 makes the output more focused and deterministic.
- **max\_tokens**: Limits the length of the generated response.
- **top\_k**: Controls the diversity of the output by sampling from the top K tokens.
- **top\_p**: Uses nucleus sampling to select tokens with a cumulative probability of `top_p`.

## 📁 File Structure

- `cli_chatbot.py`: The main script to run the chatbot.
- `config.json`: Configuration file for model parameters.
- `.env`: Environment variables, including the API key and model name.
- `requirements.txt`: List of dependencies to install.

## ❗ Error Handling

- The script gracefully handles errors related to environment variables, model initialization, and chat interaction.
- In case of an error, the script prints a descriptive message and exits.

## 🐞 Known Issues

- Currently, the chat history is not persistent between sessions.
- The `!exit` command is the only way to end the session; there is no alternative exit command.

