import pandas as pd
import re
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

# Load extracted text

class clean_text:
    def __init__(self,df,df_out,logger):
        self.df=df
        self.df=df_out
        self.logger=logger
        
    def remove(text):
        text = text.lower()  # Convert to lowercase
        text = re.sub(r"\s+", " ", text)  # Remove extra spaces
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
        text = " ".join([word for word in text.split() if word not in stopwords.words("english")])  # Remove stopwords
        return text

    def clean_text(self):
        try:
            self.df["cleaned_content"] = self.df["content"].apply(self.remove)

            # Save cleaned data
            self.df.to_csv(self.df_out, index=False)
            print("✅ Cleaned text saved!")
            self.logger.info('✅ Cleaned text saved!')

        except Exception as e:
            error_message = f"Failed to clean text: {e}"
            self.logger.error(error_message)
