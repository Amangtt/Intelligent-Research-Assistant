import os
import fitz  # PyMuPDF
import pandas as pd
from tqdm import tqdm


class get_data:

    def __init__(self,pdf_folder,output_csv,logger):
        self.pdf_folder=pdf_folder
        self.output_csv=output_csv
        self.logger=logger

    def load(self):
        data = []
        try:
            for file in tqdm(os.listdir(self.pdf_folder)):
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(self.pdf_folder, file)
                    
                    try:
                        doc = fitz.open(pdf_path)
                        text = "\n".join([page.get_text("text") for page in doc])
                        
                        data.append({"filename": file, "content": text})
                    
                    except Exception as e:
                        print(f"Error processing {file}: {e}")

            # Save to CSV for easy access later
            df = pd.DataFrame(data)
            df.to_csv(self.output_csv, index=False)
            
            self.logger.info("✅ Extracted text saved to {self.output_csv}")
        except Exception as e:
            error_message = f"Failed to extract from pdf: {e}"
            self.logger.error(error_message)