from app.app import create_app
from app.config import config_by_name

app = create_app(config_obj=config_by_name, config_name="dev")
