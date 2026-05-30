from flask import Flask, render_template, request, jsonify
from database import db, Contact

app = Flask(__name__)

# SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ryzous.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# --------------------
# WEBSITE ROUTES
# --------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# --------------------
# CONTACT FORM API
# --------------------

@app.route("/api/contact", methods=["POST"])
def submit_contact():

    data = request.get_json()

    full_name = data.get("full_name", "").strip()
    mobile = data.get("mobile", "").strip()
    email = data.get("email", "").strip()
    incident_brief = data.get("incident_brief", "").strip()

    if not full_name:
        return jsonify({
            "error": "Full name is required"
        }), 400

    if not mobile:
        return jsonify({
            "error": "Mobile number is required"
        }), 400

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    if not incident_brief:
        return jsonify({
            "error": "Incident brief is required"
        }), 400

    try:
        contact = Contact(
            full_name=full_name,
            mobile=mobile,
            email=email,
            incident_brief=incident_brief
        )

        db.session.add(contact)
        db.session.commit()

        return jsonify({
            "message": "Your request has been submitted successfully."
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

# --------------------
# VIEW ALL CONTACTS
# --------------------

@app.route("/api/contacts", methods=["GET"])
def get_contacts():

    contacts = Contact.query.order_by(
        Contact.created_at.desc()
    ).all()

    return jsonify([
        contact.to_dict()
        for contact in contacts
    ])

# --------------------
# START SERVER
# --------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )