# implemented functions

# troubles
- Choosing model for the project was a really hard, I didn't choose one so I will use CLIP and Detectron2 simultaneously.
- Everything in this project is new to me, I have to learn a lot of things.
- Many hours spend on trying to find a best way to do something, like testing CLIP, Detectron2, FasterRCNN, many datasets like yolo, coco etc; comparing anything with anything, and so on. I also have to learn how to use jupyter notebook, setup (stable) environment, figuring out not to use fancy projects like supabase. 


# update
After Grzegorz joined the project, he took front-end part, so I can focus on the back-end part. After about month I ended with testing models and I decided to use CLIP and Detectron2. I also decided to use postgres instead of sqlite. I also decided to use Flask for the web framework, and Bulma for the front-end framework, font-awesome for icons. Grzegorz insted decided to use Bootstrap for the front-end framework and javascript. I also decided to postgres as database (after a few days of testing supabase). We also decided to use Docker for the project. For end, this project is a image gallery that allows the user to upload images and then the system will detect and classify the objects on the image. The project is using the CLIP model for object detection and classification "on-time", Detectron2 for object detection and classification with object tags in database. There are many things to do, but time is running out. Anyway, I want to finish this project.

# last update
There is working connection to database with credentials from .env file, initial functions like creating database, schema, tables; essential scanning functions like hashing, uploading hash and path to database, (not tested) photos watchdog (thinking about implementing table with photo directories paths), logging to file and console, and some other functions. I also have tested two models, CLIP and Detectron2, sample implementations are in jupyter files. I am hope that I will use those samples in nearly feature. 

ps. sorry for some of the commits, I am not using git at everyday basis. 

# tools
python3.11
pip
docker
postgres
docker-compose
pyenv
importlib
jupyter
remote-ssh extension for vscode
ssh

# frameworks
Flask
flask-login
flask-uploads
flask-sqlalchemy
bulma
font-awesome
bootstrap

# libraries
os
sys
importlib
logging
hashlib
torch 
torchvision 
detectron2
clip
numpy
PIL
time
request
cv2
flask
io
dotenv
psycopg2

# references
perplexity.ai
chatgpt.com - i ask him many questions, but he don't write code for me 
https://www.youtube.com/watch?v=dam0GPOAvVI
bulma.io/documentation
some of postgres cheatsheets
many stack overflows ... 
many medium articles ...
many examples on google colab ...
tensorflow resources
