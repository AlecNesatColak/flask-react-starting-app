from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create-contact", methods=["POST"])
def create_contact():
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')
    phone = request.json.get('phone')
    address = request.json.get('address')

    if not first_name or not last_name or not email or not phone or not address:
        return  (jsonify({"error": "Missing data"}), 400,
            )
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except:
        return (jsonify({"error": "Contact already exists"}), 400)
    
    return (jsonify({"message": "Contact created"}), 201)

@app.route('/update-contact/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return (jsonify({"error": "Contact not found"}), 404)
    
    data = request.json
    contact.first_name = data.get('firstName', contact.first_name)
    contact.last_name = data.get('lastName', contact.last_name)
    contact.email = data.get('email', contact.email)
    contact.phone = data.get('phone', contact.phone)
    contact.address = data.get('address', contact.address)

    db.session.commit()
    return (jsonify({"message": "Contact updated"}), 200)

@app.route('/delete-contact/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return (jsonify({"error": "Contact not found"}), 404)
    
    db.session.delete(contact)
    db.session.commit()
    return (jsonify({"message": "Contact deleted"}), 200)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create all models in the database

    app.run(debug=True) # run the server in debug mode

