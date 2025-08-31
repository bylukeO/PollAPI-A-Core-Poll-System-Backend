# PollAPI: A Core Poll System Backend

A comprehensive RESTful API for managing polls, options, and votes built with Django and Django REST Framework. This project provides a complete backend solution for online polling applications with robust data validation, comprehensive testing, and detailed API documentation.

## 🚀 Features

- **Complete CRUD Operations**: Create, read, update, and delete polls, options, and votes
- **RESTful API Design**: Clean, intuitive endpoints following REST principles
- **Data Validation**: Comprehensive input validation with detailed error messages
- **Comprehensive Testing**: 29+ unit and integration tests covering all functionality
- **API Documentation**: Complete endpoint documentation with examples
- **Django Admin Integration**: Easy data management through Django's admin interface
- **Scalable Architecture**: Designed to handle growth and future enhancements

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET, POST | `/api/polls/` | List all polls / Create new poll |
| GET | `/api/polls/{id}/` | Get poll details |
| POST | `/api/polls/{id}/vote/` | Submit vote for poll |
| GET, POST | `/api/options/` | List all options / Create new option |
| GET, POST | `/api/polls/{id}/options/` | List poll options / Create option for poll |
| GET, PUT, DELETE | `/api/options/{id}/` | Get, update, or delete specific option |
| GET | `/api/votes/` | List all votes |

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "PollAPI A Core Poll System Backend"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux  
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`

## 📖 Usage Examples

### Create a Poll
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"question_text": "What is your favorite color?", "pub_date": "2025-08-31T12:00:00Z"}' \
http://127.0.0.1:8000/api/polls/
```

### Add Options to Poll
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"option_text": "Red", "poll": 1}' \
http://127.0.0.1:8000/api/options/
```

### Submit Vote
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"option_id": 1}' \
http://127.0.0.1:8000/api/polls/1/vote/
```

### Get Poll Results
```bash
curl http://127.0.0.1:8000/api/polls/1/
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python manage.py test
```

**Test Coverage:**
- ✅ Model tests (Poll, Option, Vote)
- ✅ API endpoint tests
- ✅ Data validation tests
- ✅ Edge case and error scenario tests
- ✅ 29 total tests with 100% pass rate

## 📊 Database Schema

### Models

**Poll**
- `id`: Primary key
- `question_text`: Poll question (max 200 chars)
- `pub_date`: Publication date

**Option**
- `id`: Primary key
- `option_text`: Option text (max 200 chars)
- `poll`: Foreign key to Poll

**Vote**
- `id`: Primary key
- `poll`: Foreign key to Poll
- `option`: Foreign key to Option

## 🔧 Data Validation

- **Poll validation**: Non-empty questions, future publication dates
- **Option validation**: Non-empty text, length limits
- **Vote validation**: Valid poll/option relationships, existence checks
- **Comprehensive error messages** for all validation failures

## 📚 Documentation

- **API Documentation**: See `API_DOCUMENTATION.md` for complete endpoint reference
- **Inline code documentation**: All classes and methods documented
- **Test documentation**: Each test case clearly documented

## 🏗 Project Structure

```
PollAPI/
├── PollAPI/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── polls/                   # Main application
│   ├── models.py           # Data models
│   ├── views.py            # API views
│   ├── serializers.py      # Data serialization
│   ├── urls.py             # URL routing
│   ├── tests.py            # Test suite
│   └── admin.py            # Admin interface
├── venv/                   # Virtual environment
├── manage.py               # Django management
├── README.md               # This file
└── API_DOCUMENTATION.md    # API reference
```

## 🔮 Future Enhancements

- User authentication and authorization
- Vote analytics and reporting
- Poll expiration dates
- Real-time results with WebSockets
- Rate limiting for vote submissions
- Email notifications
- Poll categories and tags

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

Built by LUKE OLADEJO (developedbyluke) as a capstone project for ALX AFRICA demonstrating Django REST Framework expertise, comprehensive testing practices, and API design principles.

---

**Status**: ✅ Production Ready | 📊 29 Tests Passing | 📖 Fully Documented
