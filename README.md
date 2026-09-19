## Fake Backends for Smart Gateway

This folder contains two simple FastAPI services used by the gateway for local development and testing. Each service runs on a separate port and stores its data in a local JSON file.

### Services

#### Users Service

- `GET /users` - Fetch all users
- `GET /users/{user_id}` - Fetch a single user
- `POST /users` - Create a new user
- `PATCH /users/{user_id}` - Update an existing user
- `DELETE /users/{user_id}` - Delete a user

Data file: `users/users.json`

#### Posts Service

- `GET /posts` - Fetch all posts
- `GET /posts/{post_id}` - Fetch a single post
- `POST /posts` - Create a new post
- `PATCH /posts/{post_id}` - Update an existing post
- `DELETE /posts/{post_id}` - Delete a post

Data file: `posts/posts.json`

### Run Locally

From the project root, activate the virtual environment:

```bash
source env/bin/activate
```

Start the users backend:

```bash
cd servers/users
uvicorn main:user_backend_app --host 127.0.0.1 --port 8001
```

Start the posts backend in another terminal:

```bash
cd servers/posts
uvicorn main:post_backend_app --host 127.0.0.1 --port 8002
```

### Purpose

These services are intended for:

- testing gateway routing
- testing authentication and middleware behavior
- working with mock CRUD data without a database

### What I Built And Learned

This project helped me build and demonstrate my understanding of:

- **Authentication**: validating requests and checking whether a user is allowed to access the gateway.
- **Authorization (RBAC)**: controlling access based on roles such as admin, user, and guest.
- **Rate limiting**: controlling request flow to protect backend services from excessive traffic.
- **REST API development**: building CRUD APIs for users and posts with proper HTTP methods.
- **Microservices**: running separate backend services on different ports for independent resources.
- **Proxy architecture**: forwarding requests from the gateway to the correct backend service.

In short, this setup is a practical example of how a gateway can sit in front of multiple backend services and manage routing, authentication, authorization, rate limiting, and request handling in one place.

### Notes

- Data is persisted in local JSON files.
- These services are meant for development and testing, not production use.
- Make sure both services are running before calling them through the gateway.

> If this project helped you or impressed you, feel free to **star** or **fork** it.

A Project by [Adhyatamjot Singh](https://github.com/CssAvenger)