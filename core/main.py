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



# ---------------------------------------------
# LIST + CREATE
# ---------------------------------------------
@app.get("/costs", status_code=status.HTTP_200_OK)
def list_costs():
    return costs


@app.post("/costs", status_code=status.HTTP_201_CREATED)
def create_cost(
    description: str = Query(example="cost for ...", max_length=60, min_length=5),
    amount: float = Query(example="20.20")
):
    new_id = costs[-1]["id"] + 1 if costs else 1

    cost_data = {"id": new_id, "description": description, "amount": amount}
    costs.append(cost_data)
    return JSONResponse(content=cost_data, status_code=status.HTTP_201_CREATED)


# ---------------------------------------------
# RETRIEVE + UPDATE + DELETE
# ---------------------------------------------
@app.get("/costs/{item_id}", status_code=status.HTTP_200_OK)
def get_cost(
    item_id: int = Path(description="ID of cost", example="1")
):
    for item in costs:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")


@app.put("/costs/{item_id}", status_code=status.HTTP_200_OK)
def update_cost(item_id: int, description: str, amount: float):
    for item in costs:
        if item["id"] == item_id:
            item["description"] = description
            item["amount"] = amount
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")


@app.delete("/costs/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(item_id: int):
    for i, item in enumerate(costs):
        if item["id"] == item_id:
            del costs[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="object not found")



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)