from app import create_app, db
from app.models import User, ResourceRequest, ResourceInstance

app = create_app()
app.app_context().push()

u = User.query.filter_by(username="youri").first()
for req in u.requests:
    print(req.id, req.requested_containers)
    for i in req.instances:
        print("   ->", i.name, i.ip_address)
