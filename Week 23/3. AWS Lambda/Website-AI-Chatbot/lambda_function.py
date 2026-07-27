import json
import logging
from functions import get_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):

    try:
        path = event.get("rawPath", "/")
        method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        logger.info(f"Path: {path}")
        logger.info(f"Method: {method}")

        # CORS Preflight
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": ""
            }

        # Health Check
        if path == "/health" and method == "GET":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"status": "ok"})
            }

        # Home Page
        elif path == "/" and method == "GET":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "message": "Website AI Chatbot API is running"
                })
            }

        # Chat
        elif path == "/chat" and method == "POST":

            body = json.loads(event.get("body", "{}"))

            user_message = body.get("message", "").strip()

            if not user_message:
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({
                        "reply": "Please type a message."
                    })
                }

            logger.info(f"Message: {user_message}")

            reply = get_response(user_message)

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "reply": reply
                })
            }

        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "error": "Route not found"
                })
            }

    except Exception as e:

        logger.exception(e)

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }