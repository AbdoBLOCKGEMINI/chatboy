import ollama,requests,json,re
import chainlit as cl
import datetime

import datetime

def get_current_user_time_formatted():
    """
    Get the current user's time formatted as "Wed, May 08, 7:37PM, 2024".
    """
    # Get current datetime in UTC
    current_time_utc = datetime.datetime.utcnow()

    # Convert UTC time to user's local time (assuming the user is in Dubai, which is UTC+4)
    user_time = current_time_utc + datetime.timedelta(hours=4)
    
    # Format the datetime object
    formatted_time = user_time.strftime("%a, %b %d, %I:%M%p, %Y")
    
    return formatted_time

# Example usage:
formatted_current_time = get_current_user_time_formatted()
user_location = "Deira"
system_prompt = """
1. **Introduction:**
Welcome to Rider Book! How may I assist you today? Please note: Rider Book operates exclusively within Dubai.
 To ensure a smooth experience, kindly ensure that the pick-up and drop-off locations are different and valid locations within Dubai

2. **Ride Type:**
   1. Ride Now (1)
   2. Reserve (2)
   3. Hourly (3)

 - User Must Enter All Ride Details if any miss promote user to enter the specified value for attribute
3. **Ride Now:**
    Where to? (Please provide the drop-off location)

    {Wait For User Input}

    where should we pick you up or go from?

   {Wait For User Input}

   ride details:

   - Ride Type : 
   - Pick-up Location :- 
   - Drop-off Location :- 
   - Driver :- 

   - Wait..



   
4. **Reserve:**

   -  When do you need your ride? (Thu, May 09, 06:49PM, 2024)

   {Wait For User Input}

   - Where is your destination? 

   {Wait For User Input}

    - where should we pick you up? 

    {Wait For User Input}

  - ride details:
   - Ride Type :
   - Pick-up Location:- 
   - Drop-off Location:- 
   - Scheduled Time:-  
   - Driver :- 

   - Wait..



5. **Hourly:**

   - "Would you like to schedule your ride or book now?"

   {Wait For User Input}

- Schedule for Later:

   When do you need the ride? (Thu, May 10, 06:49PM, 2024)

   {Wait For User Input}

   Where should we pick you up? 

   {Wait For User Input}

   How long do you need the ride for (Duration)? 

   {Wait For User Input}

    ride details:

   - Ride Type :
   - Pick-up Location:-
   - Scheduled Time:- 
   - Schedule Type:-
   - Driver :- 
   - Duration(Enter Number of hours):- 

   - Wait..



- Book Now:
   Where should we pick you up? 

   How long do you need the ride for? (Minimum 2 hours)

   ride details:
   - Ride Type : 
   - Pick-up Location :-
   - Duration :- 
   - Driver :-
   - Schedule Type :- 
   
- Wait..

"""


from openai import OpenAI
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def user_loc_data(formatted_current_time,user_location):
    return "Remember Location :- [{}] and Current Time [{}]  \n".format(user_location,formatted_current_time)

def drivers_api(Ride_type_value,pickup_match):
    base_url = "http://127.0.0.1:5000/"

    endpoint = "/avaliable_cars"

    url = base_url + endpoint

    response = requests.get(url)

    if response.status_code == 200:
        return  response.json()
        
        # print("Human-readable Response:")
        # print(json_response)
    else:
        print("Error:", response.status_code)
def drivers_confirmation():
    base_url = "http://127.0.0.1:5000/"

    endpoint = "/drivers_confirmation"

    url = base_url + endpoint

    response = requests.get(url)

    if response.status_code == 200:
        return  response.json()
        
        # print("Human-readable Response:")
        # print(json_response)
    else:
        print("Error:", response.status_code)
def driver_confirmation(complete_answer):
    print("Confirming :")
    
    


def Ride_Type_Data(Ride_type,complete_answer):
    print("Start...")
    print(Ride_type)

    if Ride_type:
            if "Ride Now" in Ride_type:
                pickup_match = re.search(r'Pick[\s-]*up[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                dropoff_match = re.search(r'Drop[\s-]*off[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                print("Ride Now : ")
                print("Pick-up location:", pickup_match)
                print("Drop-off location:", dropoff_match)
            if "Reserve" in Ride_type:
                scheduled_time_match = re.search(r'Scheduled[\s-]*Time\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                dropoff_match = re.search(r'Drop[\s-]*off[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                print("Reserved : ")
                print("schedule time" , scheduled_time_match)
                print("dropoff_match " , dropoff_match)
            elif "Hourly" in Ride_type:
                schedule_choice = re.search(r'Schedule[\s-]*Type\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                schedule_choice =schedule_choice.group(1)
                print("choice:", schedule_choice)
                print("Hourly :\n")
                if "Later" in schedule_choice.strip():
                    scheduled_time_match = re.search(r'Scheduled[\s-]*Time\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                    pickup_match = re.search(r'Pick[\s-]*up[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                    Duration = re.search(r'Duration\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                    print("DURATION : " , Duration.group(1))
                    print("schedule time :" , scheduled_time_match.group(1))
                    print("pickup :" , pickup_match.group(1))

                elif schedule_choice and "Book" in schedule_choice.group(1):
                    Duration = re.search(r'Duration\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                    pickup_match = re.search(r'Pick[\s-]*up[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
                    print("DURATION : " , Duration)
                    print("pick-up :" , pickup_match)
    return "Done"



def check_pickup_and_driver(complete_answer):

        # pickup_match = re.search(r'Pick-up Location :\s(.+)', complete_answer)
        # dropoff_match = re.search(r'Drop-off Location :\s(.+)', complete_answer)
        # if pickup_match is None or dropoff_match is None:
        #     pickup_match = re.search(r'Pick-up Location:\s(.+)', complete_answer)
        #     dropoff_match = re.search(r'Drop-off Location:\s(.+)', complete_answer)
        # if pickup_match is None or dropoff_match is None:
        #     pickup_match = re.search(r'Pick-up Location :-\s(.+)', complete_answer)
        #     dropoff_match = re.search(r'Drop-off Location :-\s(.+)', complete_answer)
        #     if pickup_match is None or dropoff_match is None:
        #         pickup_match = re.search(r'Pick-up Location:-\s(.+)', complete_answer)
        #         dropoff_match = re.search(r'Drop-off Location:-\s(.+)', complete_answer)
        pickup_match = re.search(r'Pick[\s-]*up[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
        # dropoff_match = re.search(r'Drop[\s-]*off[\s-]*Location\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE)
        Ride_type = re.search(r'Ride[\s-]*Type\s*[:-]?\s*([^\n]+)', complete_answer, re.IGNORECASE).group(1).replace('[', '').replace(']', '')
        print("Ride type: " , Ride_type)
        Ride_details = Ride_Type_Data(Ride_type,complete_answer)
        # track = driver_confirmation(Ride_details)
   

        
        res = drivers_api(Ride_type,pickup_match)

        # print(res)
        formatted_drivers = "" 
        
        for i, driver in enumerate(res['drivers'], start=1):
            formatted_drivers += f"Driver {i}:\n"
            formatted_drivers += f"  Name: {driver['driver_name']}\n"
            formatted_drivers += f"  Car Model: {driver['car_model']}\n"
            formatted_drivers += f"  Price: {driver['price']}\n\n"

        if formatted_drivers is None:
            formatted_drivers = ""
        print("avaliable drivers \n" ,formatted_drivers )

        return  formatted_drivers


#i want to go from dubai mall to sheikh
respone_list = []
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("chat_history", [{"role": "system",
                        "content": system_prompt}])
@cl.on_message
async def generate_response(query: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    # chat_history.append({"role": "system", "content": system_prompt})
    res = user_loc_data(formatted_current_time , user_location)
    res = res if res else ""
    cleaned_text = re.sub(r'[#<>{}\[\]/]', '', res + query.content)
    chat_history.append({"role": "user", "content":cleaned_text })
    
    response = cl.Message(content="")
    client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3'
)
    answer = client.chat.completions.create(
        model="llama3",
        messages=chat_history,stream=True ,
         temperature=0.3,
        top_p=0.9,
        max_tokens=300,
    )
    # answer = ollama.chat(model="llama3", messages=chat_history, stream=True )
    
    complete_answer = ""
    assistant = "Choose Only From Below avaliable Drivers"
    formatted_drivers = ""
    # confirmation = "Is this information correct (Enter Driver First Please)? (y/n)"
    
    for token_dict in answer:
        delta_content = token_dict.choices[0].delta.content
        token = delta_content#token_dict["message"]["content"]
        complete_answer += token
        
        await response.stream_token(token)
    
    # try:

    if "Pick-up" in complete_answer or "Drop-off" in complete_answer:
            formatted_drivers = check_pickup_and_driver(complete_answer) 
        # formatted_drivers = formatted_drivers if formatted_drivers else ""
        
    if formatted_drivers and formatted_drivers not in respone_list:
            await response.stream_token("\n**Choose Only From Below avaliable Drivers : **\n" + formatted_drivers + "e.g Drive 1 , 2")
            chat_history.append({"role": "assistant", "content": f"\n{assistant}\n{formatted_drivers}"})
            respone_list.append(formatted_drivers)
            # await response.stream_token(confirmation)
    if ("confirmation" or "confirm" in complete_answer):
        res = driver_confirmation(complete_answer)
            
    # except Exception:
    #     print("error")
    # user_message = chat_history[-2]
    # assistant_message = chat_history[-1]

    # user_content = user_message["content"]
    # assistant_content = assistant_message["content"]
    # await response.stream_token(user_content)
    # await response.stream_token(assistant_content)


    
    chat_history.append({"role": "assistant", "content": complete_answer})
    cl.user_session.set("chat_history", chat_history)

    await response.send()