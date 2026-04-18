from mcp.types import TextContent
from typing import List

class Errors:
    INVALID_SCORE = [TextContent(type="text", text=str({"status": "error", "code": "INVALID_SCORE", "message": "Score must be between 1 and 10"}))]
    NOT_FOUND = [TextContent(type="text", text=str({"status": "error", "code": "NOT_FOUND", "message": "Resource not found"}))]
    INTERNAL_ERROR = [TextContent(type="text", text=str({"status": "error", "code": "INTERNAL_ERROR", "message": "An internal error occurred"}))]
    SUCCESS_GENERIC = [TextContent(type="text", text=str({"status": "success", "message": "Operation completed successfully"}))]

class ResponseBuilder:
    @staticmethod
    def success(message: str, data: dict = None):
        res = {"status": "success", "message": message}
        if data:
            res["data"] = data
        return [TextContent(type="text", text=str(res))]

    @staticmethod
    def error(message: str, code: str = "ERROR"):
        res = {"status": "error", "code": code, "message": message}
        return [TextContent(type="text", text=str(res))]

    @staticmethod
    def generic_success():
        return ResponseBuilder.success("Operation completed successfully")

    @staticmethod
    def generic_error(msg="An unexpected error occurred"):
        return ResponseBuilder.error(msg, "GENERIC_ERROR")

    @staticmethod
    def invalid_params(msg="Invalid tool arguments"):
        return ResponseBuilder.error(msg, "INVALID_PARAMS")
