from rest_framework.response import Response

class CustomApiResponse:
    """
    A helper class for creating a standardized API response structure.
    """

    def __init__(self, status, message, data=[], code=None):
        """
        Initialize the response with status, message, data, and code.
        :param status: The status of the response (e.g., "success" or "error").
        :param message: A brief message describing the result.
        :param data: The actual data returned by the view (defaults to None).
        :param code: Optional HTTP status code (defaults to 200 for success).
        """
        self.status = status
        self.message = message
        self.data = data
        self.code = code 

    def get_response(self):
        """
        
        :return: A Response object formatted as JSON.For get succe
        """
        response_data = {
            'status_code': self.code,
            'status': self.status,
            'message': self.message,
            'data': self.data,
        }
        return Response(response_data, status=self.code)
    