from fastapi import APIRouter, Response, Request


router = APIRouter()

@router.post("/webhook/tilda")
async def tilda_webhook(request: Request):
    data = await request.json()
    # Now `data` is the payload sent by Tilda
    # You can process it as needed, for example, save it to a database
    print(data)
    return {"detail": "Webhook received"}