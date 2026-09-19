from dotenv import load_dotenv

from gateway.routes import routes

load_dotenv()

app = routes
