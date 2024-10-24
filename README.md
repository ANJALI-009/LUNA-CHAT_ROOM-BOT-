

# LUNA CHAT_ROOM BOT

## Overview

LUNA CHAT_ROOM BOT is a Streamlit web application that serves as an AI-powered assistant. It utilizes advanced language models and a FAISS-based similarity search to connect users with trainers based on their queries. The application is designed to provide seamless interactions and quick access to relevant trainer profiles.

## Features

- AI-powered chat assistant for user inquiries.
- Searchable database of trainers with relevant skills and experiences.
- Interactive buttons for easy access to trainer profiles.
- Customizable user interface with a smooth background animation.

## Technologies Used

- **Streamlit**: For building the web application interface.
- **Phi**: For AI assistant and LLM functionalities.
- **NumPy**: For efficient numerical operations.
- **FAISS**: For similarity search and clustering of embeddings.
- **Python-dotenv**: For managing environment variables.
- **Sentence Transformers**: For generating embeddings from text.
- **Pandas**: For data manipulation and reading CSV files.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/luna-chat-room-bot.git
    cd luna-chat-room-bot
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory and add your environment variables:
    ```
    API_KEY=your_api_key_here
    ```

5. **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:8501`.
2. Type your question in the input box.
3. Click the "Ask" button to receive a response from the AI assistant.
4. View related trainers based on your query and click on their profiles to chat with them.

## Data

The application fetches trainer data from a CSV file located at `data_science_profiles.csv`. Ensure this file is present in the specified directory before running the application.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- Thanks to [OpenAI](https://www.openai.com) for their research and resources on language models.
- Special thanks to the Streamlit community for their ongoing support and contributions.

## Contact

For any inquiries or feedback, feel free to reach out:

- **Your Name**: Anjali Gour
- **Email**: anjaligour.work@gmail.com
