from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from deepface import DeepFace
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
model = "SFace"
db_path = os.path.join(os.path.dirname(__file__), "faces")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing /predict/ endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        image_path = "uploaded_image.jpg"
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        dfs = DeepFace.find(
            img_path=image_path, 
            db_path=db_path, 
            model_name=model,
        )

        if len(dfs) > 0 and not dfs[0].empty:
            first_match_path = dfs[0].iloc[0]['identity']
            folder_name = os.path.basename(os.path.dirname(first_match_path))
            return JSONResponse(content={"result": True, "name": folder_name})
        else:
            raise HTTPException(status_code=404, detail="No match found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in DeepFace processing: {str(e)}")
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

@app.post("/newface/")
async def newface(file: UploadFile = File(...), name: str = Form(...)):
    try:
        # Create a folder for the person if it doesn't exist
        person_folder = os.path.join(db_path, name)
        os.makedirs(person_folder, exist_ok=True)

        # Save the uploaded image in the person's folder
        image_path = os.path.join(person_folder, file.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        return JSONResponse(content={"result": True, "message": f"New face added to {name} folder"}) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding new face: {str(e)}")
