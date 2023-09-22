import redis
import json
redis_host = 'redis-17278.c8.us-east-1-4.ec2.cloud.redislabs.com'
redis_port = 17278
redis_password = 'P9Dkhx3RktmNiBFFtOVMpzsH0uqQIWNr'


def redis_string():
    try:
        r = redis.StrictRedis(host=redis_host,port=redis_port,password=redis_password,decode_responses=True)
        r.set("message","Hello world!")
        msg=r.get("message")
        print(msg)    
    except Exception as e:
        print(e)

def sendDataToPython(json_data):
    # Parse the JSON data
    student_list = json.loads(json_data)

    redis_json_android(student_list)

   


def redis_json():
    try:
       client = redis.StrictRedis(host=redis_host,port=redis_port,password=redis_password,decode_responses=True)
       student1 = {
            'name': "logesh",
            'Age': 22,
            'Location': "Chennai"
        }
       student2 = {
            'name': "Vishwa",
            'Age': 22,
            'Location': "Chennai"
        }

       studentList = [student1, student2]
       client.json().set('studentList', '$', studentList)
       result = client.json().get('studentList')
       print(result)
    except Exception as e:
        print(e)
        

    def redis_json_android(student_list):
     try:
       client = redis.StrictRedis(host=redis_host,port=redis_port,password=redis_password,decode_responses=True)
       client.json().set('studentList2', '$', student_list)
       result = client.json().get('studentList2')
       print(result)
     except Exception as e:
        print(e)



if __name__ == "__main__":
 redis_string()
 redis_json()
