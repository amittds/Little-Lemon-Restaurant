# Little-Lemon-Restaurant-Website

Little Lemon Restaurant Website is a simple web application built using Django, designed to serve as a menu app for the Little Lemon restaurant. This repository contains the source code for the website, including HTML templates, Python code, and other assets.


## Overview

Little Lemon is a family-owned Mediterranean restaurant located in Chicago, Illinois. This website showcases the restaurant's menu, allows customers to make reservations, and provides information about the restaurant.


# Watch a Demo

https://github.com/Farahat612/Little-Lemon-Restaurant-Website/assets/67427124/e13e08cb-943e-4d24-8d77-8e543a68fbe3


## Installation

If you want to run this project locally or contribute to its development, follow these installation steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/little-lemon-restaurant-website.git
   ```
2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:

   On windows:
   ```bash
   python -m venv venv
   ```
   On macOS and Linux:
   ```bash
   source venv/bin/activate
   ``` 
4. Install the project dependencies:

   ```bash
   pip install django
   ```
5. Migrate the database:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Start the development server:

   ```bash
   python manage.py runserver
   ```
7. Visit `http://127.0.0.1:8000/` in your web browser to access the local development version of the website.


## Features

- Explore the restaurant's menu.
- Make reservations for dining.
- Learn more about the Little Lemon restaurant.
- Responsive web design for various devices.


## Skills Covered

- Django web framework.
- HTML and CSS for web development.
- Database modeling with Django models.
- Form handling and validation.
- Template rendering.
- URL routing.


## Technologies Used

- Django
- HTML5
- CSS3
- SQLite (Database)


## Contributing

Contributions to this project are welcome. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch: `$ git checkout -b my-new-branch`
3. Make your changes and commit them: `$ git commit -am 'Add some feature'`
4. Push the changes to your branch: `$ git push origin my-new-branch`
5. Submit a pull request detailing your changes.


## Known Issues or Limitations

Currently, there are no known issues or limitations with this project.


## Acknowledgments

This project was completed as part of an educational graded final assignment for `Django web Framework` course which is part of `Meta Backend Developer` Professional Certificate on Coursera. 


## License

This project is licensed under the [MIT License](LICENSE).
