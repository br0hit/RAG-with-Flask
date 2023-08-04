import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
import PyPDF2

def split_pdf(input_path, output_directory, chunk_size):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over files in the input directory
    for filename in os.listdir(input_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_path, filename)

            # Read the input PDF file
            with open(file_path, 'rb') as input_file:
                pdf = PdfFileReader(input_file)

                # Determine the total number of pages in the PDF
                total_pages = pdf.getNumPages()

                # Calculate the number of chunks
                num_chunks = total_pages // chunk_size
                if total_pages % chunk_size != 0:
                    num_chunks += 1

                # Split the PDF into chunks
                for i in range(num_chunks):
                    start_page = i * chunk_size
                    end_page = min(start_page + chunk_size, total_pages)

                    # Create a new PDF writer for each chunk
                    output_pdf = PdfFileWriter()

                    # Extract pages from the input PDF and add them to the chunk
                    for page in range(start_page, end_page):
                        output_pdf.addPage(pdf.getPage(page))

                    # Save the chunk to a new PDF file
                    output_file_path = os.path.join(output_directory, f'{filename}_chunk_{i+1}.pdf')
                    with open(output_file_path, 'wb') as output_file:
                        output_pdf.write(output_file)

                    print(f'Saved {output_file_path}')

def convert_pdf_to_txt(input_directory, output_directory):
    # Iterate over each PDF file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_directory, filename)
            txt_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")

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


def AutoConvertPDFtotext(input_directory,chunk_size, output_directory):
    
    # Create a temporary directory for storing the intermediate PDF chunks
    temp_directory = 'temp_chunks'
    split_pdf(input_directory, temp_directory, chunk_size)
        
    # Convert the PDF chunks to TXT files
    convert_pdf_to_txt(temp_directory, output_directory)
        
    # Delete the temporary directory
    shutil.rmtree(temp_directory)

    
        
##   Testing   ##


pdf_dir = "new_scrap"   
doc_dir = "sad_scrap"

AutoConvertPDFtotext(pdf_dir,2,doc_dir)
