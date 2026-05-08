STATIC_PATH = r"static"

print("Loading...")

from PIL import Image
from colorama import *
from os import system
import random, os
from flask import Flask, render_template, request

init(autoreset=True)

UNIVERSAL_LOCATIONS = ["West Stair", "East Stair", "Hudson Stair", "Bathrooms", "Escalators", "Elevators", "Water Fountains"]
seen = []

floors = [floor for floor in os.listdir(STATIC_PATH) if not floor.startswith('.')]

locations = {}
for floor in floors:
    locations[floor] = [] + UNIVERSAL_LOCATIONS
    for img in os.listdir(os.path.join(STATIC_PATH, floor)):
        location = Image.open(os.path.join(STATIC_PATH, floor, img)).getexif()[270].replace(f"{floor}/", "")
        if location not in locations[floor]:
            locations[floor].append(location)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    global seen
    if request.method == "GET" or "img" not in request.form:
        floor = random.choice(floors)
        images = [img for img in os.listdir(os.path.join(STATIC_PATH, floor)) if img not in seen]
        while len(images) == 0:
            floor = random.choice(floors)
            images = [img for img in os.listdir(os.path.join(STATIC_PATH, floor)) if img not in seen]
        selected_img = random.choice(images)
        seen.append(selected_img)
        return render_template("index.html", img=f"{floor}/{selected_img}")
    elif request.method == "POST":
        filename = request.form.get("img")
        guessed_floor = request.form.get("floor")
        floor = filename.split("/")[0]
        if "location" not in request.form:
            if guessed_floor not in floors:
                return render_template("index.html", img=filename, floor=guessed_floor, locations=UNIVERSAL_LOCATIONS)
            return render_template("index.html", img=filename, floor=guessed_floor, locations=locations[guessed_floor])
        else:
            location = request.form.get("location")
            if location == Image.open(os.path.join(STATIC_PATH, filename)).getexif()[270].replace(f"{floor}/", "") and floor == guessed_floor:
                result = True
            else:
                result = False
            return render_template("index.html", img=filename, result=result)
        
app.run()