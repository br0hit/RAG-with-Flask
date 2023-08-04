import os
from PyPDF2 import PdfFileReader, PdfFileWriter

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

# Usage example
input_directory = 'path/to/input_directory'  # Replace with the path to your input directory containing PDF files
output_directory = 'path/to/output_directory'  # Replace with the desired output directory
chunk_size = 2

split_pdf(input_directory, output_directory, chunk_size)






##################################    OLD CODE TO CONVERT A SINGLE PDF FILE INTO MULTIPLE TEXT FILES   ###########################################






# import os
# from PyPDF2 import PdfFileReader, PdfFileWriter

# def split_pdf(input_path, output_directory, chunk_size):
#     # Create output directory if it doesn't exist
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)

#     # Read the input PDF file
#     with open(input_path, 'rb') as input_file:
#         pdf = PdfFileReader(input_file)

#         # Determine the total number of pages in the PDF
#         total_pages = pdf.getNumPages()

#         # Calculate the number of chunks
#         num_chunks = total_pages // chunk_size
#         if total_pages % chunk_size != 0:
#             num_chunks += 1

#         # Split the PDF into chunks
#         for i in range(num_chunks):
#             start_page = i * chunk_size
#             end_page = min(start_page + chunk_size, total_pages)

#             # Create a new PDF writer for each chunk
#             output_pdf = PdfFileWriter()

#             # Extract pages from the input PDF and add them to the chunk
#             for page in range(start_page, end_page):
#                 output_pdf.addPage(pdf.getPage(page))

#             # Save the chunk to a new PDF file
#             output_file_path = os.path.join(output_directory, f'chunk_{i+1}.pdf')
#             with open(output_file_path, 'wb') as output_file:
#                 output_pdf.write(output_file)

#             print(f'Saved {output_file_path}')

# # Usage example
# input_path = 'new_scrap\PM-2020.pdf'  # Replace with the path to your input PDF file
# output_directory = 'final_scrap/'  # Replace with the desired output directory
# chunk_size = 2

# split_pdf(input_path, output_directory, chunk_size)
