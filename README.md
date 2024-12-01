# Project Setup

## Requirements
- **Python 3.8 or higher**
- Libraries required for this project:
  - `python-dotenv` (`pip install python-dotenv`)
  - `openai` (`pip install openai`)
  - `pandas` (`pip install pandas`)

## Installation
1. Clone the repository.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
To run this project, create a `.env` file in the root directory of the project. This file should contain the following variables:
OPENAI_API_KEY=your_openai_api_key_here

### Notes:
- Replace `your_openai_api_key_here` with your actual OpenAI API key from the [OpenAI API Dashboard](https://platform.openai.com/account/api-keys).

## Preprocessing Notes
- Comments with null or empty values are automatically removed before processing.

## Error Logging
- Errors encountered during processing are logged in `api_errors.log` by default. You can customize this in the script if needed.

## Running the Project
1. Ensure the `.env` file is correctly set up.
2. Run the main script:
   ```bash
   python TechTestCase.py