import logging
from datetime import datetime
from django.http import HttpResponse


logger = logging.getLogger(__name__)

class SimpleLoggingMiddleware:

    # Purpose: Called only once when the server starts.
    # Use: For one-time configuration, like setting up logging or reading config files.
    def __init__(self, get_response):
        self.get_response = get_response
        print("Init called")
    
    # Purpose: Called for each request. It wraps around process_request, the view, and process_response.
    # Use: Acts as the entry point of your middleware
    def __call__(self, request, *args, **kwds):
        start_time = datetime.now()
        method = request.method
        path = request.path
        logger.info(f"Request received: {method} {path} at {start_time}")

        # Get response from view
        response = self.get_response(request)

        # Code after view (process response)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response status: {response.status_code} for {method} {path} in {duration:.2f}s")

        return response
    

    # Purpose: Called before the view is called.
    # Use: Modify request, block access, log view info, or return a custom response.
    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f"About to call view: {view_func.__name__}")
        return None


    # Purpose: Called if a view raises an exception.
    # Use: Handle errors, log exceptions, send alerts.
    def process_exception(self, request, exception):
        print(f"Exception caught: {str(exception)}")
        return None

    
    # Purpose: Called for responses that support template rendering (i.e., TemplateResponse).
    # Use: Modify context before rendering the template.
    def process_template_response(self, request, response):
        print(f"template response: {str(response)}")        
        return response



class MaintenanceModeMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response
        self.maintenance = False

    def __call__(self, request ,*args, **kwds):
        if self.maintenance:
            return HttpResponse("Site is under maintenance. Please check back later.", status=503)
        return self.get_response(request)

