# TechSpec India - Gaming Laptops, GPUs & Accessories Affiliate Platform

A high-performance, AdSense-ready, and SEO-optimized static website focused on Windows Gaming Laptops, GPUs, and PC Accessories in India.

Hosted 100% free with ultra-low latency on [Cloudflare Pages](https://pages.cloudflare.com/) at `https://techspec-site.pages.dev`.

---

## 🌟 Key Features

1. **490+ Auto-Generated Static Pages:**
   - **Interactive Homepage (`/index.html`):** Real-time client-side filter by budget (Under ₹55k, ₹65k, ₹75k, ₹90k+), GPU tier (RTX 2050 to RTX 4060), and instant search.
   - **Laptop Spec & Review Pages (`/laptops/<slug>.html`):** Detailed specifications, verified TGP wattage, RAM/SSD expansion details, display color gamut (% sRGB), and tested FPS benchmarks.
   - **Head-to-Head Comparison Pages (`/compare/<slug-a>-vs-<slug-b>.html`):** Over 400 pairwise comparison tables with winner verdicts, spec differences, and Amazon CTA buttons.
   - **Curated Buying Guides (`/guides/<slug>.html`):** In-depth guides for budget segments, coding & engineering, 4K video editing, and GPU TGP deep dives.
   - **Accessories Hub & Reviews (`/accessories/`):** DDR4 & DDR5 SODIMM RAM upgrades, Gen4 NVMe SSDs, esports mice, and headsets.
   - **Trust & Compliance Pages:** `/about.html`, `/contact.html`, `/privacy-policy.html`, and `/disclaimer.html` meeting Google AdSense and Amazon Associates compliance standards.

2. **Centralized Affiliate Management:**
   - Edit `AMAZON_TAG` at the top of `dist/config.js` or in `build_site.py`:
     ```javascript
     const AMAZON_TAG = "YOUR_TAG-21";
     ```
   - Automatically tracks across all outbound Amazon.in links.

3. **Google SEO & Search Console Ready:**
   - Pre-rendered static HTML with zero JavaScript rendering delays.
   - Full OpenGraph, Twitter Cards, canonical tags, and mobile meta tags.
   - Rich JSON-LD structured data: `Product`, `FAQPage`, and `WebSite` schemas.
   - Complete `sitemap.xml` and `robots.txt` generated automatically.

---

## 🛠️ How to Rebuild the Site

Run the generator script using standard Python:

```bash
python build_site.py
```

The output will be compiled into `dist/`.

---

## 🚀 Cloudflare Pages Deployment

- **Build command:** `python build_site.py` (or leave empty if deploying pre-built `dist/`)
- **Build output directory:** `dist`
