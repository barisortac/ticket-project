### Hi!  
- I spent a little bit more than 3 hours since I enjoyed thinking about the task and implementing it; thus, I am sorry for violating this requirement. In the real sceanario, I would ask a couple of questions and challenge the use case in terms of
  - how agents complete their tasks and how we receive them?
  - is there a timeout on agents' tickets?
  - ..
- In this project, HTTP server collects ticket to assign and publishes it to RabbitMQ, then a consumer consumes those tickets and assign to the eligible Agent.
- To find the eligible agent, I defined some fields in AgentSchema -> available_for_voice_call, available_for_every_call, and total_assigned_tasks tasks. We select agents based on their total assigned task and their availability for voice & text tickets.
    - Therefore, the selection algorithm is based on the data model and usage of rabbitMQ. In rabbitMQ there are two separate queues for voice and text, and voice calls have higher priority.

### To run project
- Since I already exceeded the time, I didn't spend my time to create docker files. Since this project uses FastAPI, mongoDB and rabbitMQ, we can create a docker-compose file to make those environments available and run in parallel.
- If you want to run on your local machine, you need to have mongoDB and rabbitMQ installed in your machine. Then;
    - create `.env` file using `.env.sample` 
    - set up virtual environment, install dependencies `pip install -r requirements.txt` 
    - run FastAPI application by `uvicorn main:app --host 0.0.0.0 --port 8000`
    - run consumer by `python3 consumer/consumer.py` (you need to be on main directory of the project)
    - using openAPI of the server `http://127.0.0.1:8000/docs`, you can test the endpoint
      - you can use `mock_agent_data.js` to populate the DB (mongoDB)

### Framework selection
- In the description it was suggested to use Flask and I like it, however, I wanted to implement FastAPI since it is the framework that I used very frequently and it has openAPI defintion as default. But of course, Flask is not super different from FastAPI, it can be converted to FastAPI easily.
- For the database I used mongoDB (see Databse Selection below), and I used beanie library to communicate asyncly with mongoDB.

### Logic behind this implementation
- This server accepts tickets and publish/produce them to the rabbitmq queue, and there is a separate consumer that consumes two queues (i.e. voice_call_queue and text_based_queue) where we defined priority for them, please check config/constants.py for the definitions.
- The consumer picks the next agent based on their least assigned_tasks and their availablity for ticket types (i.e. call & text), however it can be improved. I remember in our System Design interview we used the approach of "picking agents available only for voice call", I wanted to move forward with straightforward approach of classifying agents in terms of their availability of voice call & text-based tickets.

### Database Selection
- Initially, I was thinking of setting up a SQL database (postgres) using the M2M relationship of agent & ticket language and the platform. However, I got the impression that data can be flexible, especially in terms of language.
Moreover, let's say there can be some considerations about which agent to pick, so there can be more criteria in the future.
Therefore, I chose MongoDB as the option.

### Some Ideas for Improvements
- We can have the last assigned date on the agent to evenly distribute tasks among agents.
- For seasonality, we can increase the number of consumers, or the number of tasks can assigned to the agents in the config file - of course, based on the use cases, I don't have a knowledge agent can have a maximum number of 4 calls or more.
- To mitigate the race condition of duplicate assignment to an agent (let's say 2 voice call), we can use some strategies:  
  - fetching the latest user state before updating,
  - using some caching mechanism (e.g. we set cache when we assign a ticket to an agent), of course, one of the most beautiful topics of software development is to invalidate the cache, so we need to think about when/how to invalidate the cache on that scenario.  
- We start rabbitMQ with the fastAPI startup, we can separate those.
- Right now languages are strict, we can remove the enum check there and make it super flexible.

### Package Manager
- Right now there is requirements.txt file so we use pip for libraries, but it is better to use poetry as a tool to track package dependencies 

### Testing
- This repo does not have tests yet, however there should be unit and integrational tests with mocks (actually that was the reason I tried to implement DatabaseManager, therefore we can easily mock it).
