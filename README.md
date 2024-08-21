# Chat with Documents

## Overview

This project is a web application that allows users to interact with their PDF documents by asking questions. The application uses FastAPI to handle backend processing and LangChain for document analysis and retrieval-augmented generation (RAG). Users can upload PDF files and submit queries to get answers based on the content of the uploaded documents.

## Features

- Upload PDF documents for analysis.
- Ask questions related to the content of the uploaded documents.
- Get answers and references from the documents.

## Technologies Used

- **Backend:** FastAPI
- **Document Processing:** LangChain
- **Styling:** HTML & CSS

## Setup

### Prerequisites

- Python 3.8 or higher
- Pip

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/aqibrehmanpirzada/RAG-app-with-GPT-4o-Using-Fast-API.git
    cd RAG-app-with-GPT-4o-Using-Fast-API
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Set your OpenAI API key in your environment variables:

    ```bash
    export OPENAI_API_KEY="your-openai-api-key"
    ```

### Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to `http://localhost:8000` to access the application.

## Usage

1. **Upload PDF files:** Use the file input to upload one or more PDF files.
2. **Ask a question:** Enter your query in the text input field.
3. **Submit:** Click the "Submit" button to get the answer based on the content of the uploaded documents.
4. **View Results:** The response will be displayed below the form, including the answer and source references.

## Troubleshooting

- **No response after submission:** Ensure that your OpenAI API key is correctly set and that the FastAPI server is running without errors.
- **File upload issues:** Verify that the file input accepts PDF files and that the files are not corrupted.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. For bug reports and feature requests, open an issue in the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please reach out to [aqibrehmanpirzada75@gmail.com](aqibrehmanpirzada75@gmail.com).

