from fastapi import APIRouter, Request
from services.supabase_client import get_user_tokens
from utils.token_handler import check_and_refresh_token
from services.ga4_client import get_session_count


router = APIRouter()

@router.post("/get-sessions")
async def get_sessions(request: Request):
    body = await request.json()
    
    user_id = body.get("userId")
    ga_data = body.get("googleAnalyticsData", {})
    property_id = ga_data.get("selectedProperty", {}).get("id")


    if not user_id:
        return {"error": "Missing userId in request"}
    if not property_id:
        return {"error": "Missing GA4 property ID"}
    tokens = get_user_tokens(user_id)
    if not tokens:
        return {"error": "No credentials found for this user"}
    try:
        tokens = await check_and_refresh_token(user_id, tokens)
    except Exception as e:
        return {"error": f"Token refresh failed: {str(e)}"}


    try:
        result = await get_session_count(tokens["access_token"], property_id)

        if result["value"] == "0":
            return {
                "message": "Request succeeded, but no session data found.",
                "data": result
            }

        return {
            "message": "Session count retrieved",
            "data": result
        }

    except Exception as e:
        return {
            "error": f"Google Analytics API error: {str(e)}"
        }

