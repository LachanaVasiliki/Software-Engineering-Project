Festival Management System

Overview

This project is a Festival Management System built with Django. It was developed as part of a university project to practice backend design, entity relationships, and data validation in a realistic event-management scenario.
The system focuses on organizing festivals and their performances in a clear and consistent way, rather than adding unnecessary complexity.
________________________________________
Project Goals

•	Represent festivals and performances accurately
•	Enforce correct relationships between entities
•	Apply clean and maintainable backend logic
•	Use Django features correctly and responsibly
________________________________________
What the System Does

Festival Management

•	Create and manage festivals
•	Each festival can include multiple performances
•	Validation prevents incomplete or inconsistent festival data

Performance Management

•	Performances are linked to exactly one festival
•	Required fields and relationships are validated server-side

User Access

•	Uses Django’s authentication system
•	Access to actions is controlled through permissions and application logic
________________________________________
Data Model Overview

•	Festival
o	Represents an organized event
o	Acts as the parent entity for performances

•	Performance
o	Belongs to a single festival
o	Contains scheduling and descriptive information

•	User
o	Managed through Django’s built-in authentication system

Relationships are enforced to avoid orphaned or invalid records.
________________________________________
Design & Security Considerations

•	Server-side validation for all inputs
•	No reliance on client-side checks
•	Secure default Django configuration

The system prioritizes data consistency and clear structure over feature quantity.
________________________________________
Tech Stack

•	Python
•	Django
•	Relational database (SQLite / PostgreSQL)
________________________________________
Setup:

git clone <repository-url>

cd festival-management-system

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
________________________________________
Why This Project Matters

This project shows:
•	Correct use of relational models in Django
•	Practical handling of event-based data
•	Clean separation of responsibilities in a multi-entity system

It reflects a backend-first approach focused on correctness and maintainability.

