import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal
from views import create_animal
from views import delete_animal
from views import get_all_locations, get_single_location
from views import create_location
from views import get_all_customers, get_single_customer
from views import create_customer
from views import get_all_employees, get_single_employee
from views import create_employee
from views import update_animal
from views import delete_customer, update_customer
from views import delete_employee, update_employee
from views import delete_location, update_location
from views import get_customers_by_email
from views import get_locations_by_name
from views import get_animals_by_location
from views import get_employees_by_location
from urllib.parse import urlparse, parse_qs


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]
        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # def do_GET(self):
    #     """get items"""
    #     response = {}  # Default response

    #     # Parse the URL and capture the tuple that is returned
    #     (resource, id) = self.parse_url(self.path)
    #     if resource == "animals":
    #         if id is not None:
    #             response = get_single_animal(id)
    #         else:
    #             response = get_all_animals()
    #     elif resource == "locations":
    #         if id is not None:
    #             response = get_single_location(id)
    #         else:
    #             response = get_all_locations()
    #     elif resource == "employees":
    #         if id is not None:
    #             response = get_single_employee(id)
    #         else:
    #             response = get_all_employees()
    #     elif resource == "customers":
    #         if id is not None:
    #             response = get_single_customer(id)
    #         else:
    #             response = get_all_customers()

    #     if response is not None:
    #         self._set_headers(200)
    #     else:
    #         self._set_headers(404)
    #     self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customers_by_email(query['email'][0])
            if query.get('name') and resource == 'locations':
                response = get_locations_by_name(query['name'][0])
            if query.get('location_id') and resource == 'animals':
                response = get_animals_by_location(query['location_id'][0])
            if query.get('status') and resource == 'employees':
                response = get_employees_by_location(query['location_id'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """docstring"""

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new resource
        new_resource = None
        if resource == "animals":
            if "name" in post_body and "breed" in post_body and "status" in post_body and "locationId" in post_body and "customerId" in post_body:
                new_resource = create_animal(post_body)
                self._set_headers(201)
                self.wfile.write(json.dumps(new_resource).encode())
            else:
                self._set_headers(400)
                created_resource = {
                    "message":
                        f'{"name is required, " if "name" not in post_body else ""}'
                        f'{"species is required, " if "breed" not in post_body else ""}'
                        f'{"locationId is required, " if "locationId" not in post_body else ""}'
                        f'{"customerId is required, " if "customerId" not in post_body else ""}'
                        f'{"status is required" if "status" not in post_body else ""}'
                }
                self.wfile.write(json.dumps(created_resource).encode())

        elif resource == "locations":
            if "name" in post_body and "address" in post_body:
                new_resource = create_location(post_body)
                self._set_headers(201)
                self.wfile.write(json.dumps(new_resource).encode())
            else:
                self._set_headers(400)
                created_resource = {
                    "message":
                        f'{"name is required, " if "name" not in post_body else ""}'
                        f'{"address is required" if "address" not in post_body else ""}'
                }
                self.wfile.write(json.dumps(created_resource).encode())

        elif resource == "employees":
            if "name" in post_body:
                new_resource = create_employee(post_body)
                self._set_headers(201)
                self.wfile.write(json.dumps(new_resource).encode())
            else:
                self._set_headers(400)
                created_resource = {
                    "message":
                        f'{"name is required" if "name" not in post_body else ""}'
                }
                self.wfile.write(json.dumps(created_resource).encode())

        elif resource == "customers":
            if "name" in post_body:
                new_resource = create_customer(post_body)
                self._set_headers(201)
                self.wfile.write(json.dumps(new_resource).encode())
            else:
                self._set_headers(400)
                created_resource = {
                    "message":
                        f'{"name is required" if "name" not in post_body else ""}'
                }
                self.wfile.write(json.dumps(created_resource).encode())

        else:
            self._set_headers(400)
            created_resource = {
                "message": "Invalid resource requested"
            }
            self.wfile.write(json.dumps(created_resource).encode())

    def do_DELETE(self):
        """delete animal"""
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        # Delete a single animal from the list
        if resource == "employees":
            delete_employee(id)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        # Delete a single animal from the list
        if resource == "locations":
            delete_location(id)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        # Delete a single animal from the list
        if resource == "customers":
            delete_customer(id)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        # A method that handles any PUT request.
    def do_PUT(self):
        """update animal"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        if resource == "employees":
            update_employee(id, post_body)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        if resource == "locations":
            update_location(id, post_body)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

        if resource == "customers":
            update_customer(id, post_body)

        # Encode the new animal and send in response
            self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
