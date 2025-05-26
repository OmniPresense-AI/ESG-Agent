# SASB Industry Classifier

An AI-powered tool that classifies companies into the most relevant Sustainable Accounting Standards Board (SASB) industry based on their business description.

## Features

- Uses OpenAI's GPT model for accurate industry classification
- Leverages vector search for semantic matching against SASB industry definitions
- Provides both primary industry classification and sector information
- Handles ambiguous cases with confidence scoring

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ESG-Agent.git
cd ESG-Agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the classifier:
```bash
python finder.py
```

The script will prompt for a company description and return the most relevant SASB industry classification.

## Requirements

- Python 3.8+
- OpenAI API key
- Required Python packages (see requirements.txt)

## License

MIT License 