<p align="right">
  <strong>English</strong> | <a href="./README.zh-CN.md">简体中文</a>
</p>


# Seattle Kids Weekend

A modern, responsive weekend activity aggregator tailored for families across Greater Seattle (Seattle, Eastside, North, and South Sound). The platform automates data collection from regional library networks and premier cultural landmarks, presenting curated events through an intuitive floating-card interface and interactive geospatial mapping.

> 🌐 **Live Demo**: [https://seattle-kids-weekend.vercel.app](https://seattle-kids-weekend.vercel.app)

---

## ✨ Features

- **Multi-Source Automated Ingestion Pipeline**: Consolidates schedules from the Seattle Public Library (SPL), King County Library System (KCLS Bibliocommons Gateway API), and 10+ core regional cultural landmarks (The Museum of Flight, KidsQuest Children's Museum, Burke Museum, Pacific Science Center, Seattle Aquarium, and historic farmers markets).
- **Multi-Dimensional Instant Filtering**: Supports dynamic presets (`Next 30 Days`, `This Weekend`, `Next Weekend`, `Custom Range`) alongside composite filters for sub-regions, age groups (0–5 Preschool / 6–12 Elementary), time of day (Morning/Afternoon), free admission, and indoor/rain-safe spaces.
- **Refined Floating-Card Visual Design**: Built with a calm `#f8f9fa` backdrop and isolated white floating cards with subtle shadows, pairing `Inter` and `PingFang SC` typography with optimized kerning and font weights for clean reading comfort.
- **Interactive Dual-Pane Map Sync**: Features Leaflet-powered mapping with resizable split-pane widths. Clicking an activity card smoothly pans to its map coordinate, and marker clicks isolate corresponding event details.
- **Zero-Maintenance Serverless CI/CD**: 100% static page prerendering (SSG) with scheduled data scraping via GitHub Actions and instant edge deployment via Vercel.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 16 (App Router, Turbopack), React 19, TypeScript
- **Styling**: Tailwind CSS, Lucide React
- **Mapping**: Leaflet, React-Leaflet
- **Data Engineering**: Python 3.11+ (Requests, ZoneInfo)
- **Deployment & CI/CD**: Vercel, GitHub Actions

---

## 📂 Project Structure

```text
seattle-kids-weekend/
├── .github/workflows/      # Automated weekly scraper workflow
├── public/
│   └── data/
│       └── events.geojson  # Standardized event GeoJSON dataset
├── scripts/
│   └── crawler/            # Python extraction and cleaning pipeline
│       ├── fetch_spl.py    # Seattle Public Library extractor
│       ├── fetch_kcls.py   # King County Library System API extractor
│       ├── fetch_venues.py # Landmark venue and farmers market aggregator
│       └── sync_all.py     # Aggregation, deduplication, and GeoJSON export
├── src/
│   ├── app/
│   │   ├── globals.css     # Global styles and antialiasing rules
│   │   ├── layout.tsx      # Root layout, font optimization, and metadata
│   │   └── page.tsx        # Main view, split-pane resizer, filter state
│   ├── components/
│   │   ├── DataSourceFooter.tsx # Attribution and data disclaimer footer
│   │   ├── EventList.tsx        # Scrollable event cards and detail drill-down
│   │   ├── FilterBar.tsx        # Floating multi-criteria control bar
│   │   └── LeafletMap.tsx       # Dynamic geospatial visualization
│   └── types/
│       └── event.ts        # GeoJSON schema and domain type definitions
└── package.json
```

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/<your-username>/seattle-kids-weekend.git
cd seattle-kids-weekend
npm install
```

### 2. Run the Data Pipeline

Generate the latest `events.geojson` dataset locally:

```bash
# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install requests

# Execute multi-source crawler and deduplication pipeline
python scripts/crawler/sync_all.py
```

### 3. Launch Development Server

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm run start
```

---

## 🔄 Automated Data Pipeline (CI/CD)

The project runs unattended through `.github/workflows/sync-events.yml`:
1. GitHub Actions triggers automatically on Thursdays and Saturdays (08:00 UTC / 00:00 PST).
2. The pipeline executes `scripts/crawler/sync_all.py` to pull, parse, and validate weekend schedules.
3. If new events are detected, the updated `public/data/events.geojson` is committed and pushed back to `main`.
4. The push triggers a fast, incremental static build on Vercel Edge Network, keeping live data up to date across the upcoming 30-day window.

---

## 📄 Disclaimer

All event schedules and details are gathered automatically from public domain sources and are intended solely for personal weekend trip planning. Please verify admission costs, registration requirements, and weather-related cancellations directly through official venue websites before traveling.