import logging

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

from haystack import Pipeline
from haystack.nodes import TextConverter, PDFToTextConverter
from haystack.nodes import PreProcessor
import os 

# from AutoPDFconversion import AutoConvertPDFtotext



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

# # Using inmemory document store : 
# from haystack.document_stores import InMemoryDocumentStore
# document_store = InMemoryDocumentStore(use_bm25=True)


# Check if the document store file exists
if os.path.exists("faiss_document_store.db"):
    # Delete the existing document store file
    os.remove("faiss_document_store.db")
    
    
# Using FIASS document store 
from haystack.document_stores import FAISSDocumentStore
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")

# from haystack.nodes import EmbeddingRetriever
# preprocessing_retriever = EmbeddingRetriever(document_store=document_store, embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1", model_format="sentence_transformers", top_k=20)

print("started")

indexing_pipeline = Pipeline()
# indexing_pipeline.add_node(component=PDFToConverter, name="PDFToTextConverter", inputs=["File"])
indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
indexing_pipeline.add_node(component=pre_processor, name="PreProcessor", inputs=["TextConverter"])
# indexing_pipeline.add_node(component=document_store, name="InMemoryDocs", inputs=["TextConverter"])
# indexing_pipeline.add_node(component=preprocessing_retriever, name="Retriever_for_embeddings", inputs=["PreProcessor"])
indexing_pipeline.add_node(component=document_store, name="FIASS_Docstore", inputs=["TextConverter"])


doc_dir = "sad_scrap"


files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]

for file_path in files_to_index:
    print(file_path)

# for file in files_to_index[]:
#     print(file)

print("Indexing pipeline started")
indexing_pipeline.run(file_paths=files_to_index)
print("Indexing pipeline Successfully completed")



# After creating the FIass saving it so that we dont have to run the indexing pipeline again and again once we have the data 



from haystack.nodes import EmbeddingRetriever

retriever = EmbeddingRetriever(
    document_store=document_store, embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1"
)
document_store.update_embeddings(retriever)


# # Important:
# # Now that we initialized the Retriever, we need to call update_embeddings() to iterate over all previously indexed documents and update their embedding representation.
# # While this can be a time consuming operation (depending on the corpus size), it only needs to be done once.
# # At query time, we only need to embed the query and compare it to the existing document embeddings, which is very fast.



# Save the document store:
document_store.save(index_path="data/my_index.faiss", config_path="data/my_config.json")
# Saving the document store creates two files: my_faiss_index.faiss and my_faiss_index.json


