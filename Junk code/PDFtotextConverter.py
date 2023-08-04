import os
import PyPDF2

# Set the path to the folder containing the PDF files
pdf_folder = "final_scrap/"

# Set the path to the folder where you want to store the TXT files
txt_folder = "sad_scrap/"

# Iterate over each PDF file in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        txt_path = os.path.join(txt_folder, os.path.splitext(filename)[0] + ".txt")
        
        # Convert PDF to TXT
        try:
            with open(pdf_path, "rb") as pdf_file:
                reader = PyPDF2.PdfFileReader(pdf_file)
                text = ""
                for page_num in range(reader.numPages):
                    page = reader.getPage(page_num)
                    text += page.extract_text()
            
            os.makedirs(os.path.dirname(txt_path), exist_ok=True)
            
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
                
            print(f"Successfully converted {filename} to {os.path.basename(txt_path)}")
        
        except Exception as e:
            print(f"Error converting {filename}: {e}")
