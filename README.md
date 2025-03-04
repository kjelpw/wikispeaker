# WikiSpeaker

WikiSpeaker is a Python project that fetches random Wikipedia articles, narrates them using text-to-speech, and uploads the narration to YouTube.

## Features

- Fetches random Wikipedia articles
- Retrieves article summaries and full text
- Logs major steps and errors
- Narrates articles using Google Text-to-Speech (gTTS)
- Uploads narrated articles to YouTube
- Sends and receives messages to/from ChatGPT

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/wikispeaker.git
    cd wikispeaker
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up Google API credentials for YouTube:
    - Follow the instructions [here](https://developers.google.com/youtube/v3/quickstart/python) to create a project and obtain `client_secrets.json`.
    - Save the `client_secrets.json` file in the project directory.

4. Set up OpenAI API credentials:
    - Create a `config.json` file in the project directory with the following content:
    ```json
    {
      "openai_api_key": "YOUR_OPENAI_API_KEY"
    }
    ```

## Usage

### Fetch and Narrate Wikipedia Article

To fetch a random Wikipedia article and narrate it:

```sh
python talker.py
```

### Upload Narrated Article to YouTube

To upload a narrated article to YouTube:

1. Ensure you have the `client_secrets.json` file in the project directory.
2. Run the uploader script:

```sh
python uploader.py
```

### Send and Receive Messages to/from ChatGPT

To send a message to ChatGPT and receive a response:

```sh
python chatgpt_client.py
```

## Files

- `wiki.py`: Contains the `WikipediaArticle` class for fetching Wikipedia articles.
- `talker.py`: Contains the script to fetch and narrate Wikipedia articles.
- `uploader.py`: Contains the `YouTubeUploader` class for uploading videos to YouTube.
- `chatgpt_client.py`: Contains the `ChatGPTClient` class for sending and receiving messages to/from ChatGPT.
- `README.md`: Project documentation.

## License

This project is licensed under the MIT License.