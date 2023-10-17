# Axis-Camera-HTTP-Upload-and-Notifications-Flask-App
In the Axis camera, you must create a receipt that the event will send the notifications- HTTP://IP_address//receive_notification.  Create an event for AOA to send the images and create another event to send the http notifications.  

The code establishes a hybrid server system using two separate web servers: a basic HTTP server and a Flask application. The HTTP server listens on port 5000 and is primarily designed to receive image uploads via POST requests. When an image is uploaded, it gets stored in a "static/uploads" directory with a unique timestamp-based filename. Simultaneously, the Flask application, running on port 5001, offers two functionalities. Firstly, it displays the images saved in the "static/uploads" directory when the root endpoint is accessed. Secondly, it provides an endpoint to receive notifications, which can either be a text passed as a query parameter in a GET request or a text body in a POST request. The system ensures that the two servers run concurrently by leveraging Python's threading module.
