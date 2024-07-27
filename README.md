# InsightIndia

InsightIndia is a blogging platform built with Flask that allows users to read and interact with blogs, while only admins have the ability to create and upload new blog posts. This design ensures that the content is curated and managed by authorized users, maintaining the quality and relevance of the content.

## Features

- **User Authentication**: Secure login and registration system for users.
- **Admin Dashboard**: Admins can create, edit, and delete blog posts.
- **Blog Reading**: Users can browse and read blogs.
- **Responsive Design**: Mobile-friendly layout for a seamless experience on all devices.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/anon576/InsightIndia.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd InsightIndia
   ```

3. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set Up the Database:**
   ```bash
   flask db upgrade
   ```

7. **Run the Application:**
   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.


## Usage

- **Register/Log In**: Create an account or log in to access the platform.
- **Admin Access**: Admins can access the admin dashboard to create and manage blog posts.

## Admin Instructions

- **Create/Edit/Delete Blogs**: Admins can manage blog posts from the admin dashboard. Only authorized admins have the ability to create and upload new blog posts.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

