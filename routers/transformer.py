from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/repurpose")
def repurpose_content(data: dict = Body(...)):
    # Placeholder logic – replace with your real repurposing logic here
    return {
        "status": "success",
        "message": "Content repurposed",
        "input": data
    }
