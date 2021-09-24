from elasticsearch import Elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])


class ESIndex:
    

    def create_index(self,name,properties):
        try:
            res = es.indices.create(index=name,body=properties)
            print(res['acknowledged'])
        except Exception as e:
            print(e)
    

    def list_indices(self, alias= "*"):
        try:
            a = es.indices.get_alias(alias)
            return a
        except Exception as e:
            print(e)

    

    def delete_index(self,index_name):
        try:
            res = es.indices.delete(index=index_name, ignore=[400, 404])
            print("index got deleted: ",res["acknowledged"])
        except Exception as e:
            print(e)



class ESDocument:
    def add_doc(self,index_name,doc_body):
        try:
            res = es.index(index=index_name,body=doc_body)
            print(res['acknowledged'])
        except Exception as e:
            print(e)

    def view_doc(self,index_name,id):
        try:
            res = es.get(index=index_name,id=id)
            print(res['_source'])
        except Exception as e:
            print(e)

    def update_doc(self,index_name,update_body,id):
        try:
            res = es.update(index=index_name,body=update_body,id=id)
            print("updated")
        except Exception as e:
            print(e)
    
    
    def delete_doc(self,index_name,id):
        try:
            res = es.delete(index=index_name,id=id)
            print(res['result'])
        except Exception as e:
            print(e)   


    def list_docs(self, index_name, filters_list = ["*"]):
        try:
            res= es.search(index=index_name, filter_path=filters_list)
            print("res============================", res)
            number_of_docs = res["hits"]["total"]["value"]
            docs = res["hits"]["hits"]

            return number_of_docs, docs
        except Exception as e:
            print(e)  