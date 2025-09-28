# Cuculi AI Recommendation Engine

## 1. Overview
AI-powered microservices for personalized event recommendations and behavioral nudge notifications. Converts dormant users through psychology-driven targeting.

## 2. Features
- Personalized event recommendations using vector similarity matching
- Smart user targeting with compatibility scoring
- AI-powered message generation with psychology-driven content

## 3. Architecture
- MongoDB Vector Search
- OpenAI APIs
- API microservices

## 5. API Endpoints
- `POST /api/users/{userId}/recommendations` - Event suggestions
- `POST /api/events/{eventId}/targeting` - User targeting
- `POST /api/messages/generate` - Content generation

## 6. Deployment
- **AWS Lambda**: `serverless deploy`
- **Flask Local**: `python app.py`