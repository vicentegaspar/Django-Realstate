# Real Estate Website

A full-stack real estate listing platform with Django backend and SvelteKit frontend. Admin users publish properties for sale or rent; visitors browse, search, filter, and submit inquiries.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6, Django Ninja (REST API), SQLite (dev) |
| Frontend | SvelteKit 2, Svelte 5, TypeScript |
| Styling | CSS variables, light/dark theme |

## Features

- **Property listings** – Sale and rent with images, details, and location
- **Search** – By title, address, city, region, description
- **Filters** – Listing type, property type, price, bedrooms, bathrooms, area, lot size, year built, parking, condition, pet friendly, furnished, listed date, city, region, features
- **Pagination** – 12 properties per page
- **Contact form** – Inquiries per property, visible in admin
- **Admin** – Django admin with drag-and-drop image upload
- **Theme** – Light/dark mode with system preference support

## Setup

### 1. Python environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Django setup

```bash
source venv/bin/activate
python backend/manage.py migrate
python backend/manage.py seed_data           # Property types and features
python backend/manage.py create_sample_property   # Optional: sample listings
python backend/manage.py createsuperuser     # Admin user
```

### 3. Frontend setup

```bash
cd frontend
npm install
```

## Running

**Terminal 1 – Django:**
```bash
source venv/bin/activate
python backend/manage.py runserver
```

**Terminal 2 – SvelteKit:**
```bash
cd frontend && npm run dev
```

| URL | Description |
|-----|-------------|
| http://localhost:5173 | Frontend |
| http://localhost:8000/admin/ | Django admin |
| http://localhost:8000/api/docs | API documentation |

## Adding properties

1. Log in at http://localhost:8000/admin/
2. Add a Property with status **Published**
3. Add PropertyImages: use the drag-and-drop zone above the image table, or click to browse. Drop multiple images at once.
4. Fill in details: bedrooms, bathrooms, area, lot size, year built, parking, condition, pet friendly, furnished, features
5. Properties appear on the frontend

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/properties` | GET | List properties (paginated, filterable) |
| `/api/properties/{id}` | GET | Property detail |
| `/api/properties/{id}/inquiry` | POST | Submit inquiry |
| `/api/filters` | GET | Filter options (types, features, cities, ranges) |

**Query params for `/api/properties`:** `search`, `listing_type`, `property_type`, `min_price`, `max_price`, `bedrooms`, `bathrooms`, `min_area`, `max_area`, `min_lot`, `max_lot`, `min_year`, `max_year`, `parking`, `condition`, `pet_friendly`, `furnished`, `listed_since`, `city`, `region`, `features`, `sort`, `page`

## Environment variables

| Variable | Where | Description |
|----------|-------|-------------|
| `PUBLIC_API_URL` | `frontend/.env` | API base URL (default: `http://127.0.0.1:8000/api`) |

## Project structure

```
Django-Realstate/
├── backend/
│   ├── config/              # Django settings
│   ├── properties/          # Property app
│   │   ├── models.py        # Property, PropertyType, Feature, PropertyImage, PropertyInquiry
│   │   ├── api.py           # Django Ninja endpoints
│   │   ├── admin.py         # Admin configuration
│   │   └── management/commands/
│   │       ├── seed_data.py
│   │       └── create_sample_property.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── lib/             # API client, theme, components
│   │   └── routes/          # Pages (home, properties, property detail, admin)
│   └── package.json
├── venv/
└── README.md
```

## License

MIT
