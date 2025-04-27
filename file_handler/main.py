from fastapi import FastAPI, File, UploadFile


app = FastAPI()
@app.post('/file_handler')
def upload_file(file: UploadFile = File(...)):
    #content = file.file.read()
    #size = len(content)
    filename = file.filename
    return {"filename": filename}