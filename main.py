from fastapi import FastAPI

# Create a FastAPI "instance"
app = FastAPI()

# Define a path operation decorator for the root URL ("/") and GET method
@app.get("/")
def read_root():
    # Return content that will be automatically converted to JSON
    return {"message": "Hello, World!"}

# Example with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # The item_id is validated to be an integer automatically
    return {"item_id": item_id, "q": q}
