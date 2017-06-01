class ModifyRequestMiddleware(object):
    """Emulates restrictions of the AWS Lambda + API Gateway environment"""

    def __init__(self, get_response=None):
        self.get_response = get_response
        super(ModifyRequestMiddleware, self).__init__()

    def process_request(self, request):
        # API gateway doesn't allow duplicate query string param names
        updates = [key for key in request.GET.keys() if len(request.GET.getlist(key)) > 1]
        if updates:
            updated = request.GET.copy()
            for key in updates:
                updated.setlist(key, request.GET.getlist(key)[-1])
            request.GET = updated
            request.META['QUERY_STRING'] = updated.urlencode()
            if hasattr(request, 'environ'):
                request.environ['QUERY_STRING'] = updated.urlencode()

        # Content length can't exceed 10485760 bytes
        content_length = request.META.get('CONTENT_LENGTH', '')
        max_request_size = 10485760
        if (isinstance(content_length, int) or content_length.isdigit()) and int(content_length) > max_request_size:
            raise Exception(
                'Request is too large ({0}), Lambda requires <= {1}'.format(content_length, max_request_size)
            )

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

modify_request = ModifyRequestMiddleware
