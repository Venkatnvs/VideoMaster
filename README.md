# VideoMaster
This project is a web application designed for the efficient search and processing of videos based on their subtitles. Users can upload videos, and the system automatically extracts subtitles using the ccextractor binary. The extracted subtitles are stored in Amazon DynamoDB, and the videos are stored in Amazon S3.

[![Watch the video](https://img.youtube.com/vi/qnaLAG2u7nE/hqdefault.jpg)](https://www.youtube.com/embed/qnaLAG2u7nE)
<br/>
[Watch now](https://youtu.be/qnaLAG2u7nE)

# Video Search and Processing Project

This project is a web application designed for efficient video search and processing based on subtitles. Users can upload videos, and the system automatically extracts subtitles using the ccextractor binary. The extracted subtitles are stored in Amazon DynamoDB, and the videos are stored in Amazon S3.

## Features

- **Subtitle Extraction:** Utilizes the ccextractor binary to extract subtitles from uploaded videos.
- **Storage:** Videos are stored in Amazon S3, providing scalable and secure storage. Subtitles and associated metadata are stored in Amazon DynamoDB for fast and flexible querying.
- **Search Functionality:** Allows users to search for specific words or phrases within the subtitles, providing accurate results with corresponding time segments in the video.
- **Background Processing:** Utilizes technologies like Django and Celery for efficient background processing, ensuring quick response times for HTTP requests.
- **User Interface:** The focus is on functionality rather than UI, offering a straightforward and minimalistic frontend for video upload and search operations.
- **Scalability:** Leverages Amazon Web Services (AWS) for robust and scalable cloud-based infrastructure.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Venkatnvs/VideoMaster
   ```
2. **Install Dependencies:**
   ```bash
   cd VideoMaster
   pip install -r requirements.txt
   ```
3. **Set Up AWS Credentials:**
   Configure your AWS credentials with appropriate access to S3 and DynamoDB.
4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run Celery for Background Processing:**
   ```bash
   celery -A VideoMaster worker -l info
   ```
6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the Application:**
   Open your web browser and go to http://localhost:8000/

## Usage

### Video Upload

1. Visit the home page and use the video upload form to submit videos.
2. Videos will be processed in the background, and subtitles will be extracted.

### Search

1. Use the search functionality to find specific words or phrases within the subtitles.
2. Enter keywords in the search bar and submit the query.
3. The results will provide time segments in the video where the keywords are mentioned.

### Background Processing

- Background tasks for video processing are handled using Celery.
- Adjust Celery settings in the project as needed for your deployment.

### Adjusting Celery Settings

- The Celery worker is responsible for background processing tasks.
- To adjust Celery settings, modify the `celery.py` file in the project.

## Contribution

Contributions are welcome! If you have suggestions, bug reports, or would like to contribute to the project, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
