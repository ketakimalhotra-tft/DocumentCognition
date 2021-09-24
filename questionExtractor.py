from haystack.question_generator import QuestionGenerator
from haystack.document_store import ElasticsearchDocumentStore
from haystack.pipeline import QuestionGenerationPipeline
from networkx.algorithms.link_prediction import resource_allocation_index
import es
import PyPDF2








f_path = "enter-path-to-pdf"
index_name = "seventhhaven"


def fetch_docs():
  pdfFileObject = open(f_path, 'rb')
  
  pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
  dicts = []
  print(" No. Of Pages :", pdfReader.numPages)

  for page in range(pdfReader.numPages):
      pageObject = pdfReader.getPage(page)
      dicts.append({'text':pageObject.extractText(), 'meta':{"page":page}})

  pdfFileObject.close()
  return dicts


def create_index(index_name = index_name, index_properties ={}):
  index= es.ESIndex()
  if index_name not in index.list_indices():
    index.create_index(index_name, index_properties)


def create_doc(index_name = index_name, doc_body = {}):
  document= es.ESDocument()
  count, results = document.list_docs(index_name= index_name)
  if count > 0:
    if doc_body not in results:
      document.add_doc(index_name = index_name, doc_body= doc_body)
  else:
    document.add_doc(index_name = index_name, doc_body= doc_body)


#below called only first time during server setup
'''
create_index()
doc_bodies= fetch_docs()
for doc_body in doc_bodies:
  pass
  create_doc(index_name= index_name, doc_body= doc_body)
'''

document_store = ElasticsearchDocumentStore(host="localhost", 
                                    username="", 
                                    password="", 
                                    index=index_name)

# Initialize Question Generator
question_generator = QuestionGenerator()

question_generation_pipeline = QuestionGenerationPipeline(question_generator)
for document in document_store:
        result = question_generation_pipeline.run(documents=[document])
        print("QUESTIONS",":",result['generated_questions'][0]['questions'])




