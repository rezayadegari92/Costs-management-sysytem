from fastapi import FastAPI, status, HTTPException, Path, Query
from fastapi.responses import JSONResponse
import uvicorn

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield  
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)


costs = []

@app.get("/costs_list", status_code=status.HTTP_200_OK)
def costs_list():
    return costs


@app.post("/create_cost", status_code=status.HTTP_201_CREATED)
def create_cost(description:str = Query(example="cost for ...", max_length=60, min_length=5), amount:float = Query(example="20.20")):
    if costs:
        new_id = costs[-1]["id"] + 1
    else:
        new_id = 1

    cost_data = {"id": new_id, "description": description, "amount": amount}
    costs.append(cost_data)
    return JSONResponse(content=cost_data, status_code=status.HTTP_201_CREATED)



@app.get("/cost_detail/{item_id}")
def cost_detail(item_id: int = Path(description="for get cost detail give id ", example="1")):
    for item in costs:
        if item["id"] == item_id:
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")    


@app.put("/update/{item_id}")
def update_item(item_id:int, description:str, amount:float):
    for item in costs:
        if item["id"] == item_id:
            item["description"] = description
            item["amount"] = amount
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found") 
    

@app.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for i, item in enumerate(costs):
        if item["id"] == item_id:
            del costs[i]
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)