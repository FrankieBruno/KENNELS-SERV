import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal
from views import create_animal
from views import delete_animal
from views import get_all_locations, get_single_location
from views import create_location
from views import get_all_customers, get_single_customer
from views import create_customer
from views import get_all_employees
from views import create_employee
from views.animals_requests import update_animal
from views.customers_request import delete_customer, update_customer
from views.employees_requests import delete_employee, update_employee
from views.locations_requests import delete_location, update_location


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def parse_url(self, path):
        """URL"""
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple
    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.

    def do_GET(self):
        """get items"""
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)
        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)
            else:
                response = get_all_animals()
        elif resource == "locations":
            if id is not None:
                response = get_single_location(id)
            else:
                response = get_all_locations()
        elif resource == "employees":
            if id is not None:
                response = get_single_location(id)
            else:
                response = get_all_employees()
        elif resource == "customers":
            if id is not None:
                response = get_single_customer(id)
            else:
                response = get_all_customers()

        if response is not None:
            self._set_headers(200)
        else:
            self._set_headers(404)
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
            if "name" in post_body and "species" in post_body and "status" in post_body and "locationId" in post_body and "customerId" in post_body:
                new_resource = create_animal(post_body)
                self._set_headers(201)
                self.wfile.write(json.dumps(new_resource).encode())
            else:
                self._set_headers(400)
                created_resource = {
                    "message":
                        f'{"name is required, " if "name" not in post_body else ""}'
                        f'{"species is required, " if "species" not in post_body else ""}'
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
