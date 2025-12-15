from fastapi import FastAPI, status, HTTPException, Path, Query
from fastapi.responses import JSONResponse
import uvicorn
from schemas import CostBaseSchema, CostCreateSchema, CostResponseSchema, CostUpdateSchema
from contextlib import asynccontextmanager
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield  
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)


# In-memory data store
costs: list[dict] = [{
  "description": "cost for updatign sytem",
  "amount": 2.2,
  "id": 1
}]

# -------------------------------
# LIST ALL COSTS
# -------------------------------
@app.get("/costs", response_model=List[CostResponseSchema], status_code=status.HTTP_200_OK)
def list_costs():
    return costs


# -------------------------------
# CREATE A NEW COST
# -------------------------------
@app.post("/costs", response_model=CostResponseSchema, status_code=status.HTTP_201_CREATED)
def create_cost(cost: CostCreateSchema):
    new_id = costs[-1]["id"] + 1 if costs else 1
    cost_data = cost.dict()
    cost_data["id"] = new_id
    costs.append(cost_data)
    return JSONResponse(content=cost_data, status_code=status.HTTP_201_CREATED)


# -------------------------------
# GET A SINGLE COST
# -------------------------------
@app.get("/costs/{item_id}", response_model=CostResponseSchema, status_code=status.HTTP_200_OK)
def get_cost(item_id: int):
    for item in costs:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")


# -------------------------------
# UPDATE A COST
# -------------------------------
@app.put("/costs/{item_id}", response_model=CostResponseSchema, status_code=status.HTTP_200_OK)
def update_cost(item_id: int, cost_update: CostUpdateSchema):
    for item in costs:
        if item["id"] == item_id:
            update_data = cost_update.dict(exclude_unset=True)  # Only update provided fields
            item.update(update_data)
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")


# -------------------------------
# DELETE A COST
# -------------------------------
@app.delete("/costs/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(item_id: int):
    for i, item in enumerate(costs):
        if item["id"] == item_id:
            del costs[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)