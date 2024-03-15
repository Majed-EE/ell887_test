import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template,request
import requests
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

app: Flask=Flask(__name__)
load_dotenv()
connection_string: str=os.environ.get("CONNECTION_STRING")
# connection_string=r"mongodb+srv://mongodb:mongodb@cluster0.mgbyvtz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client: MongoClient=MongoClient(connection_string)


database: Database=mongo_client.get_database("item_list")
collection: Collection=database.get_collection("item")


# item_to_add={"item_name":"test_insert_item", "item_id":77}
# collection.insert_one(item_to_add)

global URL_item, job_dict, real_job_dict
test_url=["http://127.0.0.1:5000","python-flask-webapp-ell887-test.azurewebsites.net"]
URL_item= test_url[0]
# "python-flask-webapp-ell887-test.azurewebsites.net" #"http://127.0.0.1:5000"
#'python-flask-webapp-ell887-test.azurewebsites.net'
# index_counter=10
job_dict={}
real_job_dict={}
# for x in range(index_counter):
#     job_dict[int(x+1)]=f"Item {(x+1)}"   

def item_display(item_list):
    global real_job_dict, job_dict
    for item_name in item_list:
        item=item_name["item_name"] 
        id=item_name["item_id"]
        real_id=str(item_name["_id"])
        # print("real_id")
        # print(real_id)
        # print(type(real_id))
        real_job_dict[id]={"item_name":item,"real_id":real_id}
        print(f"real item id dict \n item name {real_job_dict[id]['item_name']} \n item id {real_job_dict[id]['real_id']}")
        # real_id=item_name["_id"]
        job_dict[id]=item #"item_id":id#,"real_id":real_id} 
        # itemsz.insert(0,dict_return)
    return job_dict

 
def is_convertible_to_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False
    

def update_get_generator():
    item_list=list(collection.find()) 
        # itemsz=[]
    item_display(item_list)
#     try:
#         response = requests.get(URL_item)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return f"Error: {response.status_code}"
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
    
# def delete_function_generator(item_id):
    #generate DELETE request
    pass

def delete_function_generator(id):
    global real_job_dict
    # print(f"real jon dict is {real_job_dict}")
    # def remove_book(book_id: str):
    book_id=real_job_dict[id]["real_id"]
    print(f"book id to delete {book_id}")
    # print(f"item to delete is {real_job_dict[id]['item_name']}")
    # collection.delete_one({"_id":book_id})
    # collection.delete_one({"_id":bson.ObjectId(book_id)})
    # update_get_generator()
    string_required=URL_item+r"/items/"+book_id
    print("requireed string is ")
    print(f"{string_required}")
    # def send_delete_request(url, data=None, headers=None):
    try:
        response = requests.delete(string_required)
        return f"deleted book by the id {real_job_dict[id]}"
    except requests.exceptions.RequestException as e:
        return 500, str(e)
    
    # def delete():
    # Code to handle DELETE request
    # return 'DELETE request received!'
    # pass
# @app.route('/')
#https://python-flask-webapp-ell887-test.azurewebsites.net/items
# def index():
#     return render_template("index.html",job_dict=job_dict)
# update_get_generator()
@app.route("/",methods=["GET","POST"])
def books():
    global job_dict
    if request.method=="POST":
        # create
        if 'add_item' in request.form:
            item = request.form['item']
            item_id=request.form['item_id']
            print(f"item to add is {item}, item_id is {item_id}")

            
            if is_convertible_to_int(item_id):
                if (int(item_id) not in job_dict):
            # index_counter =index_counter+ 1
                    print(f"item id is {item_id}")
                    job_dict[int(item_id)] = item
                    collection.insert_one({"item_name":job_dict[int(item_id)], "item_id":int(item_id)})
                    # unique_id=collection.inserted_id
                    print(f"create your item {item} and id {item_id} has been added")
                    update_get_generator()
                    # db_insert(job_dict[int(item_id)],int(item_id))
                    # found_user=users.query.filter_by(item_id).first()
                    # if found_user:
                    #     pass
                    # else:
                    #     usr=users(item,item_id)
                    #     db.session.add(usr)
                    #     db.session.commit()

                else:
                    print("invalid entry: already in list")
                    # flash("invalid entry: already in list","info")
            else:
                print("invalid entry: unique id has to be integer")
                # flash("invalid entry: unique id has to be integer","info")
            # items.append(item)
        elif 'remove_item' in request.form:
                
                index_to_remove=request.form['remove_item_id']
                print(f'index to remove {index_to_remove}')
                if is_convertible_to_int(index_to_remove):
                    index_to_remove=int(index_to_remove)
                    if index_to_remove in job_dict:
                        print(f"index is {job_dict[index_to_remove]}")
                        print(delete_function_generator(index_to_remove))
                        # del job_dict[index_to_remove]
                        # db_delete(int(index_to_remove))
                    else:
                        print("Index not found")
                        # flash("Index not found")
                else:
                    print("invalid entry: unique id has to be integer","info")
                    # flash("invalid entry: unique id has to be integer","info")



            # item_name: str=request.json["item_name"]
            # item_id: int=request.json["item_id"]
            # collection.insert_one({"item_name":item_name, "item_id":item_id})
            # return render_template("index.html",job_dict=job_dict)
        
    elif request.method=="GET":
        item_list=list(collection.find()) 
        # itemsz=[]
        job_dict=item_display(item_list)
        
    return render_template("index.html",job_dict=job_dict)


@app.route("/getinfo",methods=["GET"])
def info_getter():
    if request.method=="GET":
        item_list=list(collection.find()) 
        print(item_list)
        job_dict=item_display(item_list)
        
    return job_dict#render_template("index.html",job_dict=job_dict)



@app.route("/items/<string:book_id>",methods=["PUT"])
def update_item(book_id:str):
    new_item : str=request.json["item_name"]
    new_id : int=request.json["item_id"]
    collection.update_one({"_id":bson.ObjectId(book_id)},{"$set":{"item_name":new_item, "item_id":new_id}})
    return f"inserted new book {new_item} by the id {new_id}"


@app.route("/items/<string:book_id>",methods=["DELETE"])
def remove_book(book_id: str):
    collection.delete_one({"_id":bson.ObjectId(book_id)})
    return f"deleted book by the id {book_id}"


if __name__=='__main__':
    # db.create_all()
    app.run(host='0.0.0.0',debug=True)

#az webapp up --name python-flask-webapp-ell887-test --resource-group flask-ell887-test
    


"""## Login AZ Accounts
az login --use-device-code

## Create a web app in Azure
1) Create RG
$LOCATION='eastus'
$RESOURCE_GROUP_NAME='python-flask-webapp-rg'

# Create a resource group
az group create `
    --location $LOCATION `
    --name $RESOURCE_GROUP_NAME
	
2) Create App Service Plan
$APP_SERVICE_PLAN_NAME='python-flask-webapp-plan'

az appservice plan create `
    --name $APP_SERVICE_PLAN_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --sku B1 `
    --is-linux
	
3) Create App service web app
$APP_SERVICE_NAME='python-flask-webapp-quicklabs'

az webapp create `
    --name $APP_SERVICE_NAME `
    --runtime 'PYTHON:3.9' `
    --plan $APP_SERVICE_PLAN_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --query 'defaultHostName' `
    --output table
	
	
4) Enable build automation.
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP_NAME `
    --name $APP_SERVICE_NAME `
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
	

5) Zip file upload.
az webapp deploy `
    --name $APP_SERVICE_NAME `
    --resource-group $RESOURCE_GROUP_NAME `
    --src-path F:\RekhuAll\Azure\Run_Sample_Flask_App_on_AzureWebApp\msdocs-python-flask-webapp-quickstart\msdocs-python-flask-webapp-quickstart.zip
	
6) Stream logs - Configuration
az webapp log config `
    --web-server-logging filesystem `
    --name $APP_SERVICE_NAME `
    --resource-group $RESOURCE_GROUP_NAME

7) Stream the log trail
az webapp log tail `
    --name $APP_SERVICE_NAME `
    --resource-group $RESOURCE_GROUP_NAME"""