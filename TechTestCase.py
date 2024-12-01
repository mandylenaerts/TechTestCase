import os
import pandas as pd
import logging
from dotenv import load_dotenv
from openai import (
   OpenAI, 
   # Import specific error types
   APIError,              # General API errors
   AuthenticationError,   # Issues with API key
   RateLimitError,        # API rate limit exceeded
   APIConnectionError,    # Network connectivity issues
   Timeout                # Request timed out
)

# Configure logging
logging.basicConfig(
   level=logging.ERROR,
   format='%(asctime)s - %(levelname)s - %(message)s',
   filename='api_errors.log',
   filemode='w'
)

# Load environment variables
load_dotenv()

# Set API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
   error_message = "API key not found. Check your .env file."
   logging.error(error_message)
   print(error_message)
   exit(1)

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Read the input CSV file
input_csv = "consumer_comments.csv"
data = pd.read_csv(input_csv)

# Optional preprocessing step to remove rows with null or empty comments
data = data.dropna(subset=["Comment"])  # Remove rows where 'Comment' is NaN
data = data[data["Comment"].str.strip() != ""]  # Remove rows where 'Comment' is empty or whitespace

# Define a function to process a single comment using the API
def process_comment(comment):
   try:
      # Prepare the prompt for the API
      prompt = (
            f"Analyze the following comment:\n\n"
            f"Comment: {comment}\n\n"
            "Extract the following attributes:\n"
            "- Sentiment: Positive, Neutral, or Negative. Ensure that any mention of problems (e.g., 'damaged', 'poor') results in a Negative sentiment.\n"
            "- Category: Broad category (e.g., Delivery, Customer Service, Product Quality).\n"
            " Comments like 'I received the wrong item.' should classified as 'Product Quality'.\n"
            "- Key Themes: Key points in the comment (e.g., fast delivery, damaged packaging).\n"
      )
      
      # Send the request to the API
      completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": prompt}
            ]
      )
      
      # Extract and parse the response
      response = completion.choices[0].message.content.strip()
      response_lines = response.split("\n")
      
      # Extract attributes from the response
      sentiment = response_lines[0].split(": ")[1]
      category = response_lines[1].split(": ")[1]
      key_themes = response_lines[2].split(": ")[1]
      key_themes = ", ".join([theme.strip().lower() for theme in key_themes.split(",")])
      
      return sentiment, category, key_themes

	# Handle and log API errors
   except AuthenticationError as auth_error:
      logging.error(f"Authentication Error: {auth_error}")
      raise
   except APIError as api_error:
      logging.error(f"API Error: {api_error}")
      raise
   except RateLimitError as e:
      logging.error(f"Rate limit exceeded: {e}")
      raise
   except APIConnectionError as e:
      logging.error(f"API connection error: {e}")
      raise
   except Timeout as e:
      logging.error(f"Request timed out: {e}")
      raise
   except Exception as e:
      logging.error(f"Unexpected error processing comment: {e}")
      raise

# Create an empty list to store results
results = []

# Process each comment in the dataset
for comment in data['Comment']:
   sentiment, category, key_themes = process_comment(comment)
   results.append({"Comment": comment, "Sentiment": sentiment, "Category": category, "Key Themes": key_themes})

# Convert the results to a DataFrame
output_df = pd.DataFrame(results)

# Save the output to a new CSV file
output_csv = "processed_comments.csv"
output_df.to_csv(output_csv, index=False)

print(f"Processing complete. Results saved to {output_csv}.")