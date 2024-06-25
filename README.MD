# ClearView
Just another ML for detecting and classifing objects on images packed in simple web gallery.
This project is a part of the python course at the University DSW.

# Description
The project is a image gallery that allows the user to upload images and then the system will detect and classify the objects on the image. The project is using the EfficientDet model for object detection and classification, Flask for the web framework, and Bulma for the front-end framework, font-awesome for icons.

# TODO

- [X] Choose a model [Detectron2 + CLIP]
- [X] Choose a database [Postgres]
- [X] Choose web framework [Flask]
- [X] Choose a front-end framework [Bootstrap]
- [ ] Dockerize the project
- [ ] Create report for the project (working)
- [X] Create a menu
- [ ] Create a gallery
- [ ] Create a upload form
- [ ] Create search form
- [X] Implement database initialization
- [X] Implement (some of kind?) API
- [X] Implement images scanning
- [X] Test models
- [ ] Implement models (soon will be working on it)


# Instruction | NOT WORKING YET !!! |

1. Clone the repository
2. Run in your terminal
   
```
    pip install -r requirements.txt
```

then

```
    python website/scripts/create_db.py --load-dummy-data  
```

as a result you should see

```
Database created successfully.
20 dummy photos added to the database.
```

and *instance/gallery.db* file should also be created

3. Run in your terminal

```
python website/app.py
```

and visit with your browser:

```
http://127.0.0.1:5000
```
    