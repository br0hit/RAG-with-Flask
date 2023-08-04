import logging
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

import os

from haystack import Pipeline
from haystack.nodes import TextConverter, PDFToTextConverter
from haystack.nodes import PreProcessor
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever
from AutoPDFconversion import AutoConvertToTxt
import shutil

def PreProcessing(user_docs):
    
    ######## If the text document base already exists, delete it :   #######
    if os.path.exists("txtDocs"):
    # Delete the existing document store file
        shutil.rmtree("txtDocs")
    
    AutoConvertToTxt(user_docs,2,"txtDocs")
    input_dir = "txtDocs"

    PDFToConverter = PDFToTextConverter()
    text_converter = TextConverter()

    pre_processor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
    )

    # Check if the document store file exists
    if os.path.exists("faiss_document_store.db"):
        # Delete the existing document store file
        os.remove("faiss_document_store.db")

    document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
    indexing_pipeline.add_node(component=pre_processor, name="PreProcessor", inputs=["TextConverter"])
    # indexing_pipeline.add_node(component=preprocessing_retriever, name="Retriever_for_embeddings", inputs=["PreProcessor"])
    indexing_pipeline.add_node(component=document_store, name="FAISS_Docstore", inputs=["TextConverter"])

    files_to_index = [input_dir + "/" + f for f in os.listdir(input_dir)]

    indexing_pipeline.run(file_paths=files_to_index)

    retriever = EmbeddingRetriever(
        document_store=document_store, embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1"
    )
    document_store.update_embeddings(retriever=retriever)

    if not os.path.exists("docstore"):
        os.makedirs("docstore")

    document_store.save(index_path="docstore/my_index.faiss", config_path="docstore/my_config.json")

    print("Preprocessing completed and document store saved.")
    
    # Delete the temporary directory
    shutil.rmtree("txtDocs")

# Example usage
PreProcessing("user_data")
