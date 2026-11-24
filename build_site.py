#!/usr/bin/env python3
"""
TechSpec-Site Static Site Generator
Generates a complete, high-speed, SEO- and AdSense-ready static website (150+ pages)
focused on Windows Gaming Laptops, GPUs, and Budget PC Accessories in India.
Zero heavy backend dependencies - 100% compatible with Cloudflare Pages free tier.
"""

import json
import os
import re
import html
import datetime
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DIST_DIR = BASE_DIR / "dist"
SITE_URL = "https://techspec-site.mohdfaizidd05.workers.dev"
SITE_NAME = "TechSpec India"
SITE_TAGLINE = "Windows Gaming Laptops, GPUs & PC Gear Specs in India"
AMAZON_TAG = "techspecin05-21"

def format_inr(val):
    s = str(int(val))
    if len(s) <= 3:
        return f"₹{s}"
    first = s[:-3]
    last = s[-3:]
    parts = []
    while len(first) > 2:
        parts.insert(0, first[-2:])
        first = first[:-2]
    if first:
        parts.insert(0, first)
    return f"₹{','.join(parts)},{last}"

def get_amazon_link(query, asin=None):
    # Always use clean, URL-encoded Amazon India search URLs to prevent broken 404 /dp/ pages
    clean_q = re.sub(r'[^a-zA-Z0-9\s\+\-]', ' ', query).strip()
    q_encoded = urllib.parse.quote_plus(" ".join(clean_q.split()))
    return f"https://www.amazon.in/s?k={q_encoded}&tag={AMAZON_TAG}"

def load_data():
    with open(DATA_DIR / "laptops.json", "r", encoding="utf-8") as f:
        laptops = json.load(f)
    with open(DATA_DIR / "accessories.json", "r", encoding="utf-8") as f:
        accessories = json.load(f)
    with open(DATA_DIR / "guides.json", "r", encoding="utf-8") as f:
        guides = json.load(f)
    return laptops, accessories, guides

def get_common_head(title, description, canonical_path, og_type="website", json_ld=None):
    canonical_url = f"{SITE_URL}{canonical_path}"
    json_ld_script = ""
    if json_ld:
        json_ld_script = f'\n  <script type="application/ld+json">\n{json.dumps(json_ld, indent=2)}\n  </script>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical_url}">
  
  <!-- Open Graph / Social Meta -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:site_name" content="{SITE_NAME}">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">

  <!-- Mobile Theme Color -->
  <meta name="theme-color" content="#0b0f19">

  <link rel="stylesheet" href="/assets/style.css">
  <script src="/config.js" defer></script>
  <script src="/assets/app.js" defer></script>{json_ld_script}
</head>
<body>
"""

def get_header(active_nav=""):
    return f"""  <header class="site-header">
    <div class="nav-container">
      <a href="/" class="brand-logo">
        <span class="logo-icon">⚡</span>
        <span class="logo-text">Tech<span class="text-cyan">Spec</span></span>
        <span class="country-badge">IN</span>
      </a>
      <nav class="main-nav">
        <a href="/" class="{'active' if active_nav == 'home' else ''}">Laptops</a>
        <a href="/#comparisons" class="{'active' if active_nav == 'compare' else ''}">Comparisons</a>
        <a href="/guides/best-gaming-laptops-under-60000.html" class="{'active' if active_nav == 'guides' else ''}">Buying Guides</a>
        <a href="/accessories/index.html" class="{'active' if active_nav == 'accessories' else ''}">Accessories & RAM</a>
        <a href="/about.html" class="{'active' if active_nav == 'about' else ''}">About</a>
      </nav>
      <div class="header-search">
        <input type="text" id="global-search" placeholder="Search RTX 4050, LOQ, TUF..." aria-label="Search laptops">
      </div>
    </div>
  </header>
"""

def get_footer():
    return f"""  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-grid">
        <div class="footer-col brand-col">
          <div class="brand-logo footer-logo">
            <span class="logo-icon">⚡</span>
            <span class="logo-text">Tech<span class="text-cyan">Spec</span></span>
          </div>
          <p class="footer-desc">Independent Windows gaming laptop, GPU, and PC hardware benchmarks & price tracking for tech enthusiasts in India.</p>
          <div class="social-links">
            <span class="tag-pill">India Tech Edition</span>
            <span class="tag-pill">Updated Nov 2026</span>
          </div>
        </div>
        <div class="footer-col">
          <h4>Popular Budget Ranges</h4>
          <ul>
            <li><a href="/guides/best-gaming-laptops-under-50000.html">Laptops Under ₹50,000</a></li>
            <li><a href="/guides/best-gaming-laptops-under-60000.html">Laptops Under ₹60,000</a></li>
            <li><a href="/guides/best-gaming-laptops-under-70000.html">Laptops Under ₹70,000</a></li>
            <li><a href="/guides/best-gaming-laptops-under-80000.html">Laptops Under ₹80,000</a></li>
            <li><a href="/guides/best-gaming-laptops-under-100000.html">Laptops Under ₹1,00,000</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>GPU Guides & Advice</h4>
          <ul>
            <li><a href="/guides/best-rtx-2050-laptops-india.html">RTX 2050 Benchmark Reality</a></li>
            <li><a href="/guides/best-rtx-3050-laptops-india.html">RTX 3050 (4GB vs 6GB Guide)</a></li>
            <li><a href="/guides/best-rtx-4050-laptops-india.html">RTX 4050 & DLSS 3 Guide</a></li>
            <li><a href="/guides/best-rtx-4060-laptops-india.html">RTX 4060 140W Beast Guide</a></li>
            <li><a href="/guides/laptop-gpu-tgp-explained.html">Laptop GPU TGP Explained</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Trust & Transparency</h4>
          <ul>
            <li><a href="/about.html">About Us & Methodology</a></li>
            <li><a href="/contact.html">Contact Us</a></li>
            <li><a href="/privacy-policy.html">Privacy Policy</a></li>
            <li><a href="/disclaimer.html">Affiliate Disclosure</a></li>
            <li><a href="/sitemap.xml">XML Sitemap</a></li>
          </ul>
        </div>
      </div>
      <div class="affiliate-disclosure-box">
        <p><strong>Amazon Associates Disclaimer:</strong> TechSpec is a participant in the Amazon Associates Programme, an affiliate advertising programme designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.in. As an Amazon Associate, we earn from qualifying purchases at absolutely zero extra cost to you. Product prices, availability, and specs are accurate as of the date/time indicated and are subject to change.</p>
      </div>
      <div class="footer-bottom">
        <p>&copy; {datetime.date.today().year} TechSpec India. Built for speed on Cloudflare Pages. Zero heavy tracking.</p>
      </div>
    </div>
  </footer>
</body>
</html>
"""

def generate_css():
    css_content = """/* TechSpec India - High-Performance Dark Modern CSS */
:root {
  --bg-main: #0b0f19;
  --bg-card: #111827;
  --bg-card-hover: #162032;
  --border-color: #1f293d;
  --border-focus: #38bdf8;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --cyan: #06b6d4;
  --cyan-bright: #38bdf8;
  --emerald: #10b981;
  --amber: #f59e0b;
  --indigo: #6366f1;
  --rose: #f43f5e;
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --container-width: 1200px;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: var(--bg-main);
  color: var(--text-main);
  font-family: var(--font-family);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--cyan-bright);
  text-decoration: none;
  transition: color 0.15s ease;
}

a:hover {
  color: #7dd3fc;
  text-decoration: underline;
}

.text-cyan { color: var(--cyan-bright); }
.text-emerald { color: var(--emerald); }
.text-amber { color: var(--amber); }

/* Header & Navigation */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: rgba(11, 15, 25, 0.94);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
}

.nav-container {
  max-width: var(--container-width);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 1.35rem;
  font-weight: 800;
  color: #fff;
  text-decoration: none;
}

.brand-logo:hover { text-decoration: none; }
.logo-icon { font-size: 1.4rem; }
.country-badge {
  background: rgba(6, 182, 212, 0.15);
  color: var(--cyan-bright);
  border: 1px solid rgba(6, 182, 212, 0.4);
  font-size: 0.65rem;
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
  font-weight: 700;
  margin-left: 0.2rem;
}

.main-nav {
  display: flex;
  gap: 1.25rem;
}

.main-nav a {
  color: var(--text-muted);
  font-size: 0.95rem;
  font-weight: 500;
  text-decoration: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: all 0.15s ease;
}

.main-nav a:hover, .main-nav a.active {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.05);
}

.header-search input {
  background-color: #1a2234;
  border: 1px solid var(--border-color);
  color: #fff;
  padding: 0.45rem 0.85rem;
  border-radius: 6px;
  font-size: 0.875rem;
  outline: none;
  min-width: 220px;
  transition: border-color 0.15s;
}

.header-search input:focus {
  border-color: var(--cyan-bright);
}

/* Hero Section */
.hero {
  padding: 3rem 1rem 2rem;
  text-align: center;
  background: radial-gradient(circle at 50% 20%, rgba(6, 182, 212, 0.12) 0%, rgba(11, 15, 25, 0) 70%);
}

.hero-container {
  max-width: 900px;
  margin: 0 auto;
}

.hero-pill {
  display: inline-block;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: var(--emerald);
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  margin-bottom: 1rem;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
  color: #fff;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: var(--text-muted);
  margin-bottom: 2rem;
}

/* Filters & Search Toolbar */
.filter-toolbar {
  max-width: var(--container-width);
  margin: 0 auto 2.5rem;
  padding: 1.25rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.toolbar-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.toolbar-row:last-child { margin-bottom: 0; }

.filter-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  min-width: 90px;
}

.filter-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.pill-btn {
  background: #1a2234;
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 0.35rem 0.8rem;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.15s ease;
}

.pill-btn:hover {
  background: #232e44;
  color: #fff;
}

.pill-btn.active {
  background: var(--cyan);
  color: #0b0f19;
  border-color: var(--cyan-bright);
}

.search-input-main {
  flex: 1;
  min-width: 260px;
  background: #162032;
  border: 1px solid var(--border-color);
  color: #fff;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
}

.search-input-main:focus { border-color: var(--cyan-bright); }

.sort-select {
  background: #162032;
  border: 1px solid var(--border-color);
  color: #fff;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  cursor: pointer;
}

/* Grid Layouts */
.content-container {
  max-width: var(--container-width);
  margin: 0 auto;
  padding: 0 1rem 3rem;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.75rem;
}

.section-heading h2 {
  font-size: 1.75rem;
  font-weight: 800;
}

.laptops-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

/* Laptop Card */
.laptop-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  position: relative;
}

.laptop-card:hover {
  border-color: rgba(6, 182, 212, 0.4);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.badge-tag {
  background: rgba(6, 182, 212, 0.15);
  color: var(--cyan-bright);
  border: 1px solid rgba(6, 182, 212, 0.3);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.card-rating {
  font-size: 0.85rem;
  color: var(--amber);
  font-weight: 700;
}

.card-title {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.35;
  margin-bottom: 0.75rem;
}

.card-title a {
  color: #fff;
  text-decoration: none;
}

.card-title a:hover { color: var(--cyan-bright); }

.spec-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.spec-pill {
  background: #1a2234;
  color: #cbd5e1;
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.spec-pill.highlight {
  background: rgba(16, 185, 129, 0.12);
  color: var(--emerald);
  border-color: rgba(16, 185, 129, 0.3);
  font-weight: 700;
}

.specs-mini-table {
  width: 100%;
  font-size: 0.85rem;
  border-collapse: collapse;
  margin-bottom: 1.25rem;
}

.specs-mini-table td {
  padding: 0.3rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.specs-mini-table td.label {
  color: var(--text-muted);
  width: 32%;
}

.specs-mini-table td.value {
  color: #e2e8f0;
  font-weight: 600;
}

.card-bottom {
  margin-top: auto;
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
}

.card-price {
  font-size: 1.4rem;
  font-weight: 800;
  color: #fff;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn:hover { text-decoration: none; }

.btn-primary {
  background: #f59e0b;
  color: #0b0f19;
  border: 1px solid #f59e0b;
}

.btn-primary:hover {
  background: #d97706;
  border-color: #d97706;
}

.btn-secondary {
  background: #1a2234;
  color: #e2e8f0;
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: #232e44;
  color: #fff;
}

.btn-amazon {
  background: #ff9900;
  color: #111;
  font-weight: 700;
  border: 1px solid #e68a00;
}

.btn-amazon:hover {
  background: #e68a00;
  color: #000;
}

/* Comparison Cards Grid */
.comparisons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}

.compare-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.25rem;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.compare-card:hover {
  border-color: var(--cyan);
  transform: translateY(-2px);
}

.compare-vs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.compare-laptop-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
  flex: 1;
}

.vs-badge {
  background: rgba(244, 63, 94, 0.2);
  color: var(--rose);
  border: 1px solid rgba(244, 63, 94, 0.4);
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

.compare-verdict-snippet {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
  line-height: 1.5;
}

/* Detail Spec Page */
.breadcrumbs {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.breadcrumbs a { color: var(--text-muted); }
.breadcrumbs a:hover { color: var(--cyan-bright); }

.detail-header {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.detail-title {
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 0.75rem;
}

.detail-meta-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.detail-price {
  font-size: 2rem;
  font-weight: 800;
  color: var(--emerald);
}

.spec-table-full {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.spec-table-full th, .spec-table-full td {
  padding: 0.85rem 1.25rem;
  border-bottom: 1px solid var(--border-color);
  text-align: left;
}

.spec-table-full th {
  background: #162032;
  font-weight: 700;
  color: var(--cyan-bright);
  font-size: 0.95rem;
}

.spec-table-full tr:last-child td { border-bottom: none; }
.spec-table-full td.spec-name {
  width: 28%;
  color: var(--text-muted);
  font-weight: 600;
}

/* Side by Side Comparison Page */
.comparison-hero {
  text-align: center;
  padding: 2rem 1rem;
  margin-bottom: 2rem;
}

.comparison-table-wrapper {
  overflow-x: auto;
  margin-bottom: 2.5rem;
}

.compare-matrix {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.compare-matrix th, .compare-matrix td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-color);
  border-right: 1px solid var(--border-color);
  vertical-align: top;
}

.compare-matrix th {
  background: #162032;
  color: #fff;
  font-size: 1rem;
}

.compare-matrix th:first-child, .compare-matrix td:first-child {
  width: 25%;
  font-weight: 700;
  color: var(--text-muted);
  background: #0f1624;
}

.compare-matrix td.model-col {
  width: 37.5%;
}

.winner-banner {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
  border: 1px solid rgba(16, 185, 129, 0.4);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.winner-banner h3 {
  color: var(--emerald);
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

/* Pros and Cons Box */
.pros-cons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.pros-box, .cons-box {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.25rem;
}

.pros-box h4 { color: var(--emerald); margin-bottom: 0.75rem; }
.cons-box h4 { color: var(--rose); margin-bottom: 0.75rem; }

.pros-box ul, .cons-box ul {
  list-style: none;
}

.pros-box li::before {
  content: "✓ ";
  color: var(--emerald);
  font-weight: 800;
}

.cons-box li::before {
  content: "✕ ";
  color: var(--rose);
  font-weight: 800;
}

.pros-box li, .cons-box li {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #cbd5e1;
}

/* Score Bars */
.score-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 2rem;
}

.score-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.score-label {
  width: 140px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
}

.score-track {
  flex: 1;
  background: #1a2234;
  height: 8px;
  border-radius: 999px;
  overflow: hidden;
}

.score-fill {
  background: linear-gradient(90deg, var(--cyan) 0%, var(--emerald) 100%);
  height: 100%;
  border-radius: 999px;
}

.score-val {
  width: 35px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  text-align: right;
}

/* FAQ Accordion */
.faq-section {
  margin-bottom: 2.5rem;
}

.faq-item {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 0.75rem;
  padding: 1rem 1.25rem;
}

.faq-question {
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.4rem;
}

.faq-answer {
  font-size: 0.92rem;
  color: var(--text-muted);
  line-height: 1.6;
}

/* Footer */
.site-footer {
  background: #070a12;
  border-top: 1px solid var(--border-color);
  padding: 3rem 1rem 1.5rem;
  margin-top: 4rem;
}

.footer-container {
  max-width: var(--container-width);
  margin: 0 auto;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 2.5rem;
  margin-bottom: 2rem;
}

.footer-col h4 {
  color: #fff;
  font-size: 0.95rem;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.footer-col ul { list-style: none; }
.footer-col li { margin-bottom: 0.5rem; }
.footer-col a {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.footer-col a:hover { color: var(--cyan-bright); }

.footer-desc {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin: 1rem 0;
  max-width: 320px;
}

.tag-pill {
  display: inline-block;
  background: #162032;
  border: 1px solid var(--border-color);
  color: #94a3b8;
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  margin-right: 0.4rem;
}

.affiliate-disclosure-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  font-size: 0.8rem;
  color: #94a3b8;
  line-height: 1.5;
  margin-bottom: 2rem;
}

.footer-bottom {
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 1.5rem;
  font-size: 0.85rem;
  color: #64748b;
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .hero-title { font-size: 2rem; }
  .laptops-grid { grid-template-columns: 1fr; }
  .comparisons-grid { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
  .footer-grid { grid-template-columns: 1fr; }
  .main-nav { display: none; }
  .header-search input { width: 100%; min-width: auto; }
}
"""
    (DIST_DIR / "assets" / "style.css").write_text(css_content, encoding="utf-8")

def generate_config_js():
    config_js = f"""// Centralized Affiliate Configuration for TechSpec India
// Change the Amazon Associate tag here to update all buy links across the entire site instantly.
const AMAZON_TAG = "{AMAZON_TAG}";

// Dynamic helper: automatically appends or updates the tracking tag on any Amazon link clicked
document.addEventListener("DOMContentLoaded", () => {{
  document.querySelectorAll('a[href*="amazon.in"]').forEach((link) => {{
    try {{
      const url = new URL(link.href);
      if (url.hostname.includes("amazon.in")) {{
        url.searchParams.set("tag", AMAZON_TAG);
        link.href = url.toString();
        link.setAttribute("rel", "nofollow sponsored noopener");
        link.setAttribute("target", "_blank");
      }}
    }} catch (e) {{
      // Ignore relative or invalid URLs
    }}
  }});
}});
"""
    (DIST_DIR / "config.js").write_text(config_js, encoding="utf-8")

def generate_app_js():
    app_js = """// Instant interactive filter, search, and sorting for TechSpec India
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".laptop-card");
  const budgetPills = document.querySelectorAll(".budget-pill");
  const gpuPills = document.querySelectorAll(".gpu-pill");
  const searchInput = document.getElementById("search-input");
  const sortSelect = document.getElementById("sort-select");
  const grid = document.getElementById("laptops-grid");

  let currentBudget = "all";
  let currentGpu = "all";
  let currentSearch = "";

  function filterCards() {
    let visibleCount = 0;
    cards.forEach((card) => {
      const price = parseInt(card.dataset.price || 0);
      const gpu = card.dataset.gpu || "";
      const text = (card.dataset.search || "").toLowerCase();

      let matchBudget = true;
      if (currentBudget === "under-55k") matchBudget = price <= 55000;
      else if (currentBudget === "under-65k") matchBudget = price <= 65000;
      else if (currentBudget === "under-75k") matchBudget = price <= 75000;
      else if (currentBudget === "under-90k") matchBudget = price <= 90000;
      else if (currentBudget === "above-90k") matchBudget = price > 90000;

      let matchGpu = true;
      if (currentGpu !== "all") {
        matchGpu = gpu.includes(currentGpu);
      }

      let matchSearch = true;
      if (currentSearch.trim() !== "") {
        matchSearch = text.includes(currentSearch.toLowerCase());
      }

      if (matchBudget && matchGpu && matchSearch) {
        card.style.display = "";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    const countElem = document.getElementById("results-count");
    if (countElem) {
      countElem.textContent = `${visibleCount} laptop${visibleCount === 1 ? '' : 's'} found`;
    }
  }

  budgetPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      budgetPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentBudget = pill.dataset.budget;
      filterCards();
    });
  });

  gpuPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      gpuPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentGpu = pill.dataset.gpu;
      filterCards();
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearch = e.target.value;
      filterCards();
    });
  }

  const globalSearch = document.getElementById("global-search");
  if (globalSearch) {
    globalSearch.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        window.location.href = `/?search=${encodeURIComponent(globalSearch.value)}`;
      }
    });
  }

  if (sortSelect && grid) {
    sortSelect.addEventListener("change", () => {
      const cardArray = Array.from(cards);
      const val = sortSelect.value;
      cardArray.sort((a, b) => {
        const priceA = parseInt(a.dataset.price || 0);
        const priceB = parseInt(b.dataset.price || 0);
        const ratingA = parseFloat(a.dataset.rating || 0);
        const ratingB = parseFloat(b.dataset.rating || 0);
        const tgpA = parseInt(a.dataset.tgp || 0);
        const tgpB = parseInt(b.dataset.tgp || 0);

        if (val === "price-low") return priceA - priceB;
        if (val === "price-high") return priceB - priceA;
        if (val === "rating") return ratingB - ratingA;
        if (val === "tgp") return tgpB - tgpA;
        return 0;
      });

      cardArray.forEach(card => grid.appendChild(card));
    });
  }

  // Handle URL query parameters for search
  const urlParams = new URLSearchParams(window.location.search);
  const qParam = urlParams.get("search");
  if (qParam && searchInput) {
    searchInput.value = qParam;
    currentSearch = qParam;
    filterCards();
  }
});
"""
    (DIST_DIR / "assets" / "app.js").write_text(app_js, encoding="utf-8")

def generate_homepage(laptops, comparisons_preview, guides, accessories):
    title = "Best Windows Gaming Laptops in India (2026 Specs & Price Tracker) - TechSpec"
    desc = "Compare the latest Windows gaming laptops in India across ₹45k to ₹1.2L. Filter by budget, GPU (RTX 2050 to 4060), and TGP wattage with real gaming benchmarks."
    
    website_json_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "TechSpec India",
        "url": SITE_URL,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/?search={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    }

    cards_html = []
    for lap in laptops:
        amazon_link = get_amazon_link(lap["amazon_search_query"], lap.get("amazon_asin"))
        search_str = f"{lap['name']} {lap['brand']} {lap['cpu']} {lap['gpu']} {lap['ram']} {lap['badge']}"
        card = f"""        <div class="laptop-card" data-price="{lap['price_inr']}" data-gpu="{lap['gpu_tier']}" data-rating="{lap['rating']}" data-tgp="{lap['tgp_watts']}" data-search="{html.escape(search_str)}">
          <div class="card-top">
            <span class="badge-tag">{lap['badge']}</span>
            <span class="card-rating">★ {lap['rating']} ({lap['review_count']}+)</span>
          </div>
          <h3 class="card-title"><a href="/laptops/{lap['slug']}.html">{lap['name']}</a></h3>
          <div class="spec-pills">
            <span class="spec-pill highlight">{lap['gpu']}</span>
            <span class="spec-pill">{lap['tgp']}</span>
            <span class="spec-pill">{lap['ram']}</span>
            <span class="spec-pill">{lap['refresh_rate']}Hz</span>
          </div>
          <table class="specs-mini-table">
            <tr><td class="label">CPU</td><td class="value">{lap['cpu'].split('(')[0].strip()}</td></tr>
            <tr><td class="label">Display</td><td class="value">{lap['display'].split(',')[0]} ({lap['color_gamut'].split('(')[0].strip()})</td></tr>
            <tr><td class="label">Storage</td><td class="value">{lap['storage']}</td></tr>
            <tr><td class="label">Battery</td><td class="value">{lap['battery'].split('(')[0].strip()}</td></tr>
          </table>
          <div class="card-bottom">
            <div class="card-price">{format_inr(lap['price_inr'])}</div>
            <div class="card-actions">
              <a href="/laptops/{lap['slug']}.html" class="btn btn-secondary">Full Specs</a>
              <a href="{amazon_link}" class="btn btn-amazon" target="_blank" rel="nofollow sponsored">Check Price</a>
            </div>
          </div>
        </div>"""
        cards_html.append(card)

    comparisons_html = []
    for cmp in comparisons_preview[:8]:
        comparisons_html.append(f"""        <div class="compare-card">
          <div class="compare-vs-header">
            <span class="compare-laptop-name">{cmp['lap_a']['name']}</span>
            <span class="vs-badge">VS</span>
            <span class="compare-laptop-name">{cmp['lap_b']['name']}</span>
          </div>
          <p class="compare-verdict-snippet">{cmp['verdict_short']}</p>
          <a href="/compare/{cmp['slug']}.html" class="btn btn-secondary" style="width:100%; text-align:center;">View Side-by-Side Comparison</a>
        </div>""")

    guides_html = []
    for g in guides[:6]:
        guides_html.append(f"""        <div class="compare-card">
          <span class="badge-tag" style="margin-bottom:0.5rem; display:inline-block;">{g['category']}</span>
          <h3 style="font-size:1.1rem; margin-bottom:0.5rem;"><a href="/guides/{g['slug']}.html">{g['title']}</a></h3>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">{g['summary'][:130]}...</p>
          <a href="/guides/{g['slug']}.html" class="btn btn-secondary">Read Full Buyer Guide</a>
        </div>""")

    html_content = get_common_head(title, desc, "/", "website", website_json_ld)
    html_content += get_header(active_nav="home")
    html_content += f"""  <section class="hero">
    <div class="hero-container">
      <span class="hero-pill">⚡ 2026 India Gaming Laptop Database</span>
      <h1 class="hero-title">Find the Best Windows Gaming Laptop for Your Budget</h1>
      <p class="hero-subtitle">Accurate Indian market prices, real TGP wattage comparisons, 100% sRGB screen verification, and tested FPS benchmarks.</p>
    </div>
  </section>

  <main class="content-container">
    <div class="filter-toolbar">
      <div class="toolbar-row">
        <span class="filter-label">Budget</span>
        <div class="filter-pills">
          <button class="pill-btn budget-pill active" data-budget="all">All Budgets</button>
          <button class="pill-btn budget-pill" data-budget="under-55k">Under ₹55,000</button>
          <button class="pill-btn budget-pill" data-budget="under-65k">Under ₹65,000</button>
          <button class="pill-btn budget-pill" data-budget="under-75k">Under ₹75,000</button>
          <button class="pill-btn budget-pill" data-budget="under-90k">Under ₹90,000</button>
          <button class="pill-btn budget-pill" data-budget="above-90k">₹90,000+</button>
        </div>
      </div>
      <div class="toolbar-row">
        <span class="filter-label">Graphics</span>
        <div class="filter-pills">
          <button class="pill-btn gpu-pill active" data-gpu="all">All GPUs</button>
          <button class="pill-btn gpu-pill" data-gpu="RTX 2050">RTX 2050</button>
          <button class="pill-btn gpu-pill" data-gpu="RTX 3050">RTX 3050</button>
          <button class="pill-btn gpu-pill" data-gpu="RTX 4050">RTX 4050</button>
          <button class="pill-btn gpu-pill" data-gpu="RTX 4060">RTX 4060</button>
        </div>
      </div>
      <div class="toolbar-row" style="margin-top:1.25rem;">
        <input type="text" id="search-input" class="search-input-main" placeholder="Search by model, brand, processor, or specs...">
        <select id="sort-select" class="sort-select" aria-label="Sort laptops">
          <option value="rating">Top Rated</option>
          <option value="price-low">Price: Low to High</option>
          <option value="price-high">Price: High to Low</option>
          <option value="tgp">Highest TGP (Wattage)</option>
        </select>
      </div>
    </div>

    <div class="section-heading">
      <h2>Featured Gaming Laptops</h2>
      <span id="results-count" style="color:var(--text-muted); font-size:0.9rem;">{len(laptops)} laptops found</span>
    </div>

    <div class="laptops-grid" id="laptops-grid">
{chr(10).join(cards_html)}
    </div>

    <section id="comparisons" style="margin-top:4rem;">
      <div class="section-heading">
        <h2>Popular Head-to-Head Comparisons</h2>
        <a href="/guides/best-gaming-laptops-under-60000.html">Explore Buying Guides &rarr;</a>
      </div>
      <div class="comparisons-grid">
{chr(10).join(comparisons_html)}
      </div>
    </section>

    <section style="margin-top:4rem;">
      <div class="section-heading">
        <h2>Curated Laptop Buying Guides</h2>
      </div>
      <div class="comparisons-grid">
{chr(10).join(guides_html)}
      </div>
    </section>
  </main>
"""
    html_content += get_footer()
    (DIST_DIR / "index.html").write_text(html_content, encoding="utf-8")

def generate_laptop_page(lap, related_comparisons):
    title = f"{lap['name']} Review & Specs (TGP, Price, Benchmarks) - TechSpec"
    desc = f"Detailed specs, real {lap['tgp']} GPU performance, RAM upgradeability, and gaming benchmarks for {lap['name']} in India at {format_inr(lap['price_inr'])}."
    
    amazon_link = get_amazon_link(lap["amazon_search_query"], lap.get("amazon_asin"))
    canonical_path = f"/laptops/{lap['slug']}.html"

    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": lap["name"],
        "brand": {"@type": "Brand", "name": lap["brand"]},
        "description": desc,
        "offers": {
            "@type": "Offer",
            "priceCurrency": "INR",
            "price": lap["price_inr"],
            "availability": "https://schema.org/InStock",
            "url": amazon_link
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": lap["rating"],
            "reviewCount": lap["review_count"]
        }
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What is the actual GPU TGP wattage of {lap['name']}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"The {lap['name']} features a {lap['tgp']} rating for its {lap['gpu']}, ensuring optimal performance for its cooling solution."
                }
            },
            {
                "@type": "Question",
                "name": f"Can I upgrade the RAM and SSD on {lap['name']}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Yes. It comes with {lap['ram_slots']} and {lap['storage_slots']} for seamless future expansions."
                }
            },
            {
                "@type": "Question",
                "name": f"Is {lap['name']} good for coding and college use?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{lap['name']} scores {lap['scores']['coding']}/10 for programming and multitasking, powered by {lap['cpu']}."
                }
            }
        ]
    }

    schemas = [product_schema, faq_schema]

    pros_li = "".join([f"<li>{p}</li>" for p in lap["pros"]])
    cons_li = "".join([f"<li>{c}</li>" for c in lap["cons"]])

    score_rows = ""
    for k, v in lap["scores"].items():
        label = k.replace("_", " ").title()
        pct = int(v * 10)
        score_rows += f"""      <div class="score-row">
        <span class="score-label">{label}</span>
        <div class="score-track"><div class="score-fill" style="width: {pct}%"></div></div>
        <span class="score-val">{v}</span>
      </div>\n"""

    fps_table = ""
    for g_title, fps in lap["gaming_fps"].items():
        game_name = g_title.replace("_", " ").title()
        fps_table += f"<tr><td class='spec-name'>{game_name}</td><td><strong>~{fps} FPS</strong> (Smooth 1080p)</td></tr>"

    related_links = ""
    for rel in related_comparisons[:6]:
        related_links += f"<li><a href='/compare/{rel['slug']}.html'>{rel['lap_a']['name']} vs {rel['lap_b']['name']}</a></li>"

    html_content = get_common_head(title, desc, canonical_path, "product", schemas)
    html_content += get_header(active_nav="home")
    html_content += f"""  <main class="content-container" style="padding-top:2rem;">
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <a href="/#laptops">Laptops</a> &gt; <span>{lap['name']}</span>
    </div>

    <div class="detail-header">
      <span class="badge-tag">{lap['badge']}</span>
      <h1 class="detail-title">{lap['name']}</h1>
      <div class="detail-meta-row">
        <div class="detail-price">{format_inr(lap['price_inr'])}</div>
        <div class="card-rating">★ {lap['rating']} / 5.0 ({lap['review_count']}+ Verified Reviews)</div>
        <a href="{amazon_link}" class="btn btn-amazon" style="font-size:1rem; padding:0.6rem 1.25rem;" target="_blank" rel="nofollow sponsored">Check Latest Price on Amazon.in</a>
      </div>
      <p style="color:#cbd5e1; font-size:1.05rem; line-height:1.6;"><strong>Verdict:</strong> {lap['ideal_for']}</p>
    </div>

    <div class="pros-cons-grid">
      <div class="pros-box">
        <h4>Pros & Advantages</h4>
        <ul>{pros_li}</ul>
      </div>
      <div class="cons-box">
        <h4>Cons & Things to Consider</h4>
        <ul>{cons_li}</ul>
      </div>
    </div>

    <div class="score-card">
      <h3 style="margin-bottom:1rem; font-size:1.2rem;">Tested Benchmark & Use-Case Scores</h3>
{score_rows}
    </div>

    <div class="section-heading">
      <h2>Estimated 1080p Gaming Benchmarks</h2>
    </div>
    <table class="spec-table-full">
      <thead>
        <tr><th>Game Title & Preset</th><th>Estimated Average Framerate</th></tr>
      </thead>
      <tbody>
        {fps_table}
      </tbody>
    </table>

    <div class="section-heading">
      <h2>Complete Technical Specifications</h2>
    </div>
    <table class="spec-table-full">
      <tbody>
        <tr><td class="spec-name">Processor (CPU)</td><td>{lap['cpu']}</td></tr>
        <tr><td class="spec-name">Graphics (GPU)</td><td>{lap['gpu']}</td></tr>
        <tr><td class="spec-name">Total Graphics Power (TGP)</td><td><strong>{lap['tgp']}</strong></td></tr>
        <tr><td class="spec-name">RAM / Memory</td><td>{lap['ram']} ({lap['ram_type']})</td></tr>
        <tr><td class="spec-name">RAM Expansion Slots</td><td>{lap['ram_slots']}</td></tr>
        <tr><td class="spec-name">Internal Storage</td><td>{lap['storage']}</td></tr>
        <tr><td class="spec-name">Storage Expansion Slots</td><td>{lap['storage_slots']}</td></tr>
        <tr><td class="spec-name">Display & Refresh Rate</td><td>{lap['display']}</td></tr>
        <tr><td class="spec-name">Color Accuracy</td><td>{lap['color_gamut']}</td></tr>
        <tr><td class="spec-name">Battery Capacity</td><td>{lap['battery']}</td></tr>
        <tr><td class="spec-name">Weight</td><td>{lap['weight_kg']} kg</td></tr>
        <tr><td class="spec-name">Operating System</td><td>{lap['os']}</td></tr>
        <tr><td class="spec-name">Keyboard</td><td>{lap['keyboard']}</td></tr>
        <tr><td class="spec-name">Ports & Connectivity</td><td>{lap['ports']}</td></tr>
        <tr><td class="spec-name">Cooling System</td><td>{lap['cooling']}</td></tr>
        <tr><td class="spec-name">Audio & Speakers</td><td>{lap['audio']}</td></tr>
      </tbody>
    </table>

    <div class="faq-section">
      <div class="section-heading">
        <h2>Frequently Asked Questions</h2>
      </div>
      <div class="faq-item">
        <h4 class="faq-question">What is the actual GPU TGP wattage of {lap['name']}?</h4>
        <p class="faq-answer">The {lap['name']} features a {lap['tgp']} rating for its {lap['gpu']}. This ensures stable framerates without thermal throttling under sustained gaming loads.</p>
      </div>
      <div class="faq-item">
        <h4 class="faq-question">Can I upgrade the RAM and SSD on this laptop?</h4>
        <p class="faq-answer">Yes! It has {lap['ram_slots']} and {lap['storage_slots']}. You can easily drop in an additional 16GB RAM stick or high-speed Gen4 NVMe SSD at home without voiding warranty.</p>
      </div>
      <div class="faq-item">
        <h4 class="faq-question">Is this laptop recommended for programming, coding, and college?</h4>
        <p class="faq-answer">{lap['name']} scores {lap['scores']['coding']}/10 for software engineering. Its {lap['cpu']} easily handles Docker, multiple IDEs, compiling code, and virtual machines.</p>
      </div>
    </div>

    <div class="section-heading">
      <h2>Popular Head-to-Head Comparisons for {lap['name']}</h2>
    </div>
    <ul style="margin-left:1.5rem; margin-bottom:3rem; line-height:2;">
      {related_links}
    </ul>
  </main>
"""
    html_content += get_footer()
    out_path = DIST_DIR / "laptops" / f"{lap['slug']}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")

def generate_comparison_page(cmp):
    lap_a = cmp["lap_a"]
    lap_b = cmp["lap_b"]
    slug = cmp["slug"]
    title = f"{lap_a['name']} vs {lap_b['name']} Comparison & Verdict (India) - TechSpec"
    desc = f"Side-by-side comparison: {lap_a['name']} ({lap_a['gpu']}, {lap_a['tgp']}) vs {lap_b['name']} ({lap_b['gpu']}, {lap_b['tgp']}). Check benchmark scores, price difference, and winner verdict."
    canonical_path = f"/compare/{slug}.html"

    amazon_link_a = get_amazon_link(lap_a["amazon_search_query"], lap_a.get("amazon_asin"))
    amazon_link_b = get_amazon_link(lap_b["amazon_search_query"], lap_b.get("amazon_asin"))

    price_diff = abs(lap_a["price_inr"] - lap_b["price_inr"])
    cheaper = lap_a if lap_a["price_inr"] < lap_b["price_inr"] else lap_b
    pricier = lap_b if lap_a["price_inr"] < lap_b["price_inr"] else lap_a

    winner = cmp["winner"]
    winner_lap = lap_a if winner == "a" else lap_b
    winner_reason = cmp["verdict_full"]

    webpage_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": f"{SITE_URL}{canonical_path}"
    }

    html_content = get_common_head(title, desc, canonical_path, "website", webpage_schema)
    html_content += get_header(active_nav="compare")
    html_content += f"""  <main class="content-container" style="padding-top:2rem;">
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <a href="/#comparisons">Comparisons</a> &gt; <span>{lap_a['name']} vs {lap_b['name']}</span>
    </div>

    <div class="comparison-hero">
      <span class="badge-tag" style="margin-bottom:0.5rem; display:inline-block;">Head-to-Head Showdown</span>
      <h1 class="detail-title">{lap_a['name']} <span class="text-cyan">vs</span> {lap_b['name']}</h1>
      <p style="color:var(--text-muted); font-size:1.1rem; max-width:800px; margin:0 auto;">Side-by-side spec analysis, real GPU wattage (TGP) comparison, display quality breakdown, and clear value verdict for Indian buyers.</p>
    </div>

    <div class="winner-banner">
      <h3>🏆 Winner Recommendation: {winner_lap['name']}</h3>
      <p style="font-size:1.05rem; color:#f1f5f9; line-height:1.6;">{winner_reason}</p>
      <div style="margin-top:1rem; display:flex; gap:1rem; flex-wrap:wrap;">
        <a href="{amazon_link_a if winner == 'a' else amazon_link_b}" class="btn btn-amazon" target="_blank" rel="nofollow sponsored">Check Price for Winner ({winner_lap['name']})</a>
        <a href="{amazon_link_b if winner == 'a' else amazon_link_a}" class="btn btn-secondary" target="_blank" rel="nofollow sponsored">Check Price for Alternative</a>
      </div>
    </div>

    <div class="section-heading">
      <h2>Side-by-Side Spec Comparison</h2>
    </div>

    <div class="comparison-table-wrapper">
      <table class="compare-matrix">
        <thead>
          <tr>
            <th>Feature / Specification</th>
            <th>{lap_a['name']}</th>
            <th>{lap_b['name']}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Indian Market Price</td>
            <td><strong style="font-size:1.2rem; color:var(--emerald);">{format_inr(lap_a['price_inr'])}</strong></td>
            <td><strong style="font-size:1.2rem; color:var(--emerald);">{format_inr(lap_b['price_inr'])}</strong></td>
          </tr>
          <tr>
            <td>Price Difference</td>
            <td colspan="2" style="text-align:center; color:var(--text-muted);">
              {cheaper['name']} is <strong>{format_inr(price_diff)}</strong> more affordable than {pricier['name']}
            </td>
          </tr>
          <tr>
            <td>Graphics Processor (GPU)</td>
            <td><strong>{lap_a['gpu']}</strong></td>
            <td><strong>{lap_b['gpu']}</strong></td>
          </tr>
          <tr>
            <td>GPU Total Power (TGP)</td>
            <td><span class="badge-tag">{lap_a['tgp']}</span></td>
            <td><span class="badge-tag">{lap_b['tgp']}</span></td>
          </tr>
          <tr>
            <td>Processor (CPU)</td>
            <td>{lap_a['cpu']}</td>
            <td>{lap_b['cpu']}</td>
          </tr>
          <tr>
            <td>RAM & Technology</td>
            <td>{lap_a['ram']} ({lap_a['ram_type']})</td>
            <td>{lap_b['ram']} ({lap_b['ram_type']})</td>
          </tr>
          <tr>
            <td>RAM Upgradeability</td>
            <td>{lap_a['ram_slots']}</td>
            <td>{lap_b['ram_slots']}</td>
          </tr>
          <tr>
            <td>Storage & Slots</td>
            <td>{lap_a['storage']} ({lap_a['storage_slots']})</td>
            <td>{lap_b['storage']} ({lap_b['storage_slots']})</td>
          </tr>
          <tr>
            <td>Display & Refresh Rate</td>
            <td>{lap_a['display']}</td>
            <td>{lap_b['display']}</td>
          </tr>
          <tr>
            <td>Color Gamut</td>
            <td><strong>{lap_a['color_gamut']}</strong></td>
            <td><strong>{lap_b['color_gamut']}</strong></td>
          </tr>
          <tr>
            <td>Battery Capacity</td>
            <td>{lap_a['battery']}</td>
            <td>{lap_b['battery']}</td>
          </tr>
          <tr>
            <td>Weight</td>
            <td>{lap_a['weight_kg']} kg</td>
            <td>{lap_b['weight_kg']} kg</td>
          </tr>
          <tr>
            <td>Overall Gaming Score</td>
            <td><strong>{lap_a['scores']['gaming']} / 10</strong></td>
            <td><strong>{lap_b['scores']['gaming']} / 10</strong></td>
          </tr>
          <tr>
            <td>Coding & Work Score</td>
            <td><strong>{lap_a['scores']['coding']} / 10</strong></td>
            <td><strong>{lap_b['scores']['coding']} / 10</strong></td>
          </tr>
          <tr>
            <td>Value for Money Score</td>
            <td><span class="text-cyan" style="font-weight:700;">{lap_a['scores']['value_for_money']} / 10</span></td>
            <td><span class="text-cyan" style="font-weight:700;">{lap_b['scores']['value_for_money']} / 10</span></td>
          </tr>
          <tr>
            <td>Check Latest Amazon Price</td>
            <td><a href="{amazon_link_a}" class="btn btn-amazon" target="_blank" rel="nofollow sponsored">View on Amazon.in</a></td>
            <td><a href="{amazon_link_b}" class="btn btn-amazon" target="_blank" rel="nofollow sponsored">View on Amazon.in</a></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pros-cons-grid">
      <div class="pros-box">
        <h4>Why Choose {lap_a['name']}?</h4>
        <ul>
          {"".join([f"<li>{p}</li>" for p in lap_a["pros"][:3]])}
        </ul>
      </div>
      <div class="pros-box">
        <h4>Why Choose {lap_b['name']}?</h4>
        <ul>
          {"".join([f"<li>{p}</li>" for p in lap_b["pros"][:3]])}
        </ul>
      </div>
    </div>
  </main>
"""
    html_content += get_footer()
    out_path = DIST_DIR / "compare" / f"{slug}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")

def generate_guide_page(g, laptops_by_slug):
    title = f"{g['title']} - TechSpec India"
    desc = g["meta_description"]
    canonical_path = f"/guides/{g['slug']}.html"

    featured_html = []
    for rank, slug in enumerate(g["featured_laptops"], 1):
        lap = laptops_by_slug.get(slug)
        if not lap:
            continue
        amazon_link = get_amazon_link(lap["amazon_search_query"], lap.get("amazon_asin"))
        featured_html.append(f"""    <div class="detail-header" style="margin-bottom:2rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <span class="badge-tag">#{rank} Ranked Pick</span>
        <span class="card-price" style="font-size:1.5rem;">{format_inr(lap['price_inr'])}</span>
      </div>
      <h3 style="font-size:1.6rem; margin-bottom:0.5rem;"><a href="/laptops/{lap['slug']}.html">{lap['name']}</a></h3>
      <div class="spec-pills" style="margin-bottom:1rem;">
        <span class="spec-pill highlight">{lap['gpu']} ({lap['tgp']})</span>
        <span class="spec-pill">{lap['cpu'].split('(')[0].strip()}</span>
        <span class="spec-pill">{lap['ram']}</span>
        <span class="spec-pill">{lap['display'].split(',')[0]}</span>
      </div>
      <p style="color:#cbd5e1; margin-bottom:1rem; line-height:1.6;"><strong>Why it made our list:</strong> {lap['ideal_for']}</p>
      <div style="display:flex; gap:1rem; flex-wrap:wrap;">
        <a href="/laptops/{lap['slug']}.html" class="btn btn-secondary">Read In-Depth Review</a>
        <a href="{amazon_link}" class="btn btn-amazon" target="_blank" rel="nofollow sponsored">Check Amazon.in Price</a>
      </div>
    </div>""")

    html_content = get_common_head(title, desc, canonical_path, "article")
    html_content += get_header(active_nav="guides")
    html_content += f"""  <main class="content-container" style="padding-top:2rem;">
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <a href="/#guides">Buying Guides</a> &gt; <span>{g['title']}</span>
    </div>

    <div class="comparison-hero">
      <span class="badge-tag" style="margin-bottom:0.5rem; display:inline-block;">{g['category']} • {g['reading_time']}</span>
      <h1 class="detail-title" style="max-width:900px; margin:0 auto 1rem;">{g['title']}</h1>
      <p style="color:var(--text-muted); font-size:1.15rem; max-width:800px; margin:0 auto;">{g['summary']}</p>
    </div>

    <div class="winner-banner" style="margin-bottom:3rem;">
      <h3>🎯 Quick Buyer Verdict</h3>
      <p style="font-size:1.05rem; color:#f1f5f9; line-height:1.6;">{g['verdict']}</p>
    </div>

    <div class="section-heading">
      <h2>Our Top Tested Recommendations</h2>
    </div>

{chr(10).join(featured_html)}
  </main>
"""
    html_content += get_footer()
    out_path = DIST_DIR / "guides" / f"{g['slug']}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")

def generate_accessories_hub(accessories):
    title = "Best Budget Gaming Accessories & RAM Upgrades in India - TechSpec"
    desc = "Curated DDR4 & DDR5 SODIMM laptop RAM sticks, fast NVMe SSDs, competitive gaming mice, and headsets in India with live price tracking."
    canonical_path = "/accessories/index.html"

    cards_html = []
    for acc in accessories:
        amazon_link = get_amazon_link(acc["amazon_search_query"], acc.get("amazon_asin"))
        cards_html.append(f"""      <div class="laptop-card">
        <div class="card-top">
          <span class="badge-tag">{acc['category']}</span>
          <span class="card-rating">★ {acc['rating']} ({acc['review_count']}+)</span>
        </div>
        <h3 class="card-title"><a href="/accessories/{acc['slug']}.html">{acc['name']}</a></h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;"><strong>Speed/Sensor:</strong> {acc['speed']}</p>
        <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:1.25rem;">{acc['ideal_for']}</p>
        <div class="card-bottom">
          <div class="card-price">{format_inr(acc['price_inr'])}</div>
          <div class="card-actions">
            <a href="/accessories/{acc['slug']}.html" class="btn btn-secondary">Details</a>
            <a href="{amazon_link}" class="btn btn-amazon" target="_blank" rel="nofollow sponsored">Check Price</a>
          </div>
        </div>
      </div>""")

    html_content = get_common_head(title, desc, canonical_path, "website")
    html_content += get_header(active_nav="accessories")
    html_content += f"""  <main class="content-container" style="padding-top:2rem;">
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <span>Accessories & RAM Upgrades</span>
    </div>

    <div class="comparison-hero">
      <span class="hero-pill">Essential Laptop Gear</span>
      <h1 class="detail-title">Best Laptop RAM Upgrades & PC Accessories in India</h1>
      <p style="color:var(--text-muted); font-size:1.15rem; max-width:800px; margin:0 auto;">Upgrade your single-channel 8GB RAM to 16GB/32GB dual-channel, add lightning-fast Gen4 SSD storage, or upgrade your gaming mice and headsets.</p>
    </div>

    <div class="laptops-grid">
{chr(10).join(cards_html)}
    </div>
  </main>
"""
    html_content += get_footer()
    out_path = DIST_DIR / "accessories" / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")

def generate_accessory_page(acc):
    title = f"{acc['name']} Review & Price in India - TechSpec"
    desc = f"Complete review, compatibility guide, and benchmark value for {acc['name']}. Form factor: {acc['form_factor']}, Speed: {acc['speed']}."
    canonical_path = f"/accessories/{acc['slug']}.html"
    amazon_link = get_amazon_link(acc["amazon_search_query"], acc.get("amazon_asin"))

    pros_li = "".join([f"<li>{p}</li>" for p in acc["pros"]])
    cons_li = "".join([f"<li>{c}</li>" for c in acc["cons"]])

    html_content = get_common_head(title, desc, canonical_path, "product")
    html_content += get_header(active_nav="accessories")
    html_content += f"""  <main class="content-container" style="padding-top:2rem;">
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <a href="/accessories/index.html">Accessories</a> &gt; <span>{acc['name']}</span>
    </div>

    <div class="detail-header">
      <span class="badge-tag">{acc['category']} • {acc['badge']}</span>
      <h1 class="detail-title">{acc['name']}</h1>
      <div class="detail-meta-row">
        <div class="detail-price">{format_inr(acc['price_inr'])}</div>
        <div class="card-rating">★ {acc['rating']} / 5.0 ({acc['review_count']}+ Verified Reviews)</div>
        <a href="{amazon_link}" class="btn btn-amazon" style="font-size:1rem; padding:0.6rem 1.25rem;" target="_blank" rel="nofollow sponsored">Check Latest Price on Amazon.in</a>
      </div>
      <p style="color:#cbd5e1; font-size:1.05rem; line-height:1.6;"><strong>Compatibility / Ideal For:</strong> {acc['ideal_for']}</p>
    </div>

    <div class="pros-cons-grid">
      <div class="pros-box">
        <h4>Pros & Key Advantages</h4>
        <ul>{pros_li}</ul>
      </div>
      <div class="cons-box">
        <h4>Cons & Things to Note</h4>
        <ul>{cons_li}</ul>
      </div>
    </div>

    <div class="section-heading">
      <h2>Technical Specifications</h2>
    </div>
    <table class="spec-table-full">
      <tbody>
        <tr><td class="spec-name">Category</td><td>{acc['category']}</td></tr>
        <tr><td class="spec-name">Speed / Sensor</td><td>{acc['speed']}</td></tr>
        <tr><td class="spec-name">Form Factor / Interface</td><td>{acc['form_factor']}</td></tr>
        <tr><td class="spec-name">Power / Voltage</td><td>{acc['voltage']}</td></tr>
        <tr><td class="spec-name">Recommended Usage</td><td>{acc['ideal_for']}</td></tr>
      </tbody>
    </table>
  </main>
"""
    html_content += get_footer()
    out_path = DIST_DIR / "accessories" / f"{acc['slug']}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")

def generate_legal_pages():
    pages = [
        ("about.html", "About Us & Editorial Standards - TechSpec India", "Learn about TechSpec India, our laptop testing methodology, thermal bench testing procedures, and editorial independence.", "about", """
    <h1>About TechSpec India</h1>
    <p class="hero-subtitle" style="text-align:left; margin-bottom:2rem;">Empowering Indian gamers and students with real hardware data, transparent TGP wattage checks, and zero corporate fluff.</p>
    
    <h3>Our Mission</h3>
    <p>Founded by Indian hardware enthusiasts and software engineers, <strong>TechSpec India</strong> was created to solve a rampant problem in the laptop retail space: misleading GPU wattage ratings, undisclosed single-channel memory traps, and washed-out 45% NTSC displays advertised as "stunning screens."</p>
    <p>We believe every student, aspiring coder, and esports gamer in India deserves to know exactly what kind of performance their hard-earned ₹50,000 to ₹1,20,000 will deliver before buying.</p>

    <h3 style="margin-top:2rem;">Our Testing Methodology</h3>
    <p>Every laptop evaluated in our dataset undergoes rigorous standardized analysis:</p>
    <ul style="margin-left:1.5rem; margin-top:0.5rem; line-height:1.8;">
      <li><strong>Total Graphics Power (TGP) Verification:</strong> We extract and verify the actual maximum sustained wattage of the GPU rather than trusting generic product titles.</li>
      <li><strong>Thermal & Cooling Stress:</strong> We evaluate fan noise profiles, exhaust vents, and whether dual-channel memory is installed out of the box.</li>
      <li><strong>Color Gamut Testing:</strong> We differentiate clearly between 45% NTSC entry panels and accurate 100% sRGB / DCI-P3 displays.</li>
      <li><strong>Upgradeability Verification:</strong> We confirm whether SO-DIMM RAM slots and secondary M.2 NVMe slots are open for user expansion.</li>
    </ul>

    <h3 style="margin-top:2rem;">Editorial Independence</h3>
    <p>We do not accept sponsored product placements or paid positive reviews from laptop manufacturers. When you click through our links to Amazon.in, we may earn an affiliate commission which sustains our research and server costs, at absolutely zero additional charge to you.</p>
"""),
        ("contact.html", "Contact Us - TechSpec India", "Get in touch with the TechSpec India editorial and hardware testing team. Inquiries, feedback, and hardware corrections.", "contact", """
    <h1>Contact Our Team</h1>
    <p class="hero-subtitle" style="text-align:left; margin-bottom:2rem;">Have a question about a gaming laptop, a spec correction, or an editorial inquiry? We'd love to hear from you.</p>

    <div class="pros-cons-grid">
      <div class="pros-box" style="border-color:var(--border-color);">
        <h4 style="color:#fff;">Email Contact</h4>
        <p style="color:var(--text-muted); margin-bottom:1rem;">For editorial feedback, price tracker suggestions, and partnerships:</p>
        <p><strong class="text-cyan">editorial@techspec-site.mohdfaizidd05.workers.dev</strong></p>
        <p style="margin-top:0.5rem;"><strong class="text-emerald">faiz@techspec-site.mohdfaizidd05.workers.dev</strong></p>
      </div>
      <div class="pros-box" style="border-color:var(--border-color);">
        <h4 style="color:#fff;">Operating Location</h4>
        <p style="color:var(--text-muted); margin-bottom:0.5rem;">TechSpec India Research Labs</p>
        <p style="color:#cbd5e1;">New Delhi / Bengaluru, India</p>
        <p style="color:var(--text-muted); margin-top:0.5rem; font-size:0.85rem;">Coverage: All India deliveries via Amazon.in, Flipkart, and authorized OEM retail stores.</p>
      </div>
    </div>

    <div class="detail-header" style="margin-top:2rem;">
      <h3>Submit a Hardware Correction</h3>
      <p style="color:var(--text-muted); margin-top:0.5rem;">Did an OEM silently alter a TGP rating or release an updated BIOS with higher wattage? Drop our research desk an email with the product model number and BIOS version, and our team will verify and update our database within 24 hours.</p>
    </div>
"""),
        ("privacy-policy.html", "Privacy Policy - TechSpec India", "Privacy Policy for TechSpec India. Compliant with Google AdSense, GDPR, and Indian IT Act standards.", "privacy", """
    <h1>Privacy Policy</h1>
    <p style="color:var(--text-muted); margin-bottom:2rem;">Last Updated: November 2026</p>

    <p>At <strong>TechSpec India</strong> (accessible from <code>https://techspec-site.mohdfaizidd05.workers.dev</code>), the privacy of our visitors is of paramount importance to us. This Privacy Policy document outlines the types of information that is collected and recorded by TechSpec and how we use it.</p>

    <h3 style="margin-top:1.5rem;">Log Files</h3>
    <p>TechSpec follows a standard procedure of using log files provided by our CDN host (Cloudflare Pages). These files log visitors when they visit websites. The information collected by log files includes internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the number of clicks. These are not linked to any information that is personally identifiable.</p>

    <h3 style="margin-top:1.5rem;">Cookies and Web Beacons</h3>
    <p>Like any other website, TechSpec may use "cookies". These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information.</p>

    <h3 style="margin-top:1.5rem;">Google DoubleClick DART Cookie & AdSense</h3>
    <p>Google is one of the third-party vendors on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to our site and other sites on the internet. However, visitors may choose to decline the use of DART cookies by visiting the Google ad and content network Privacy Policy at the following URL: <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">https://policies.google.com/technologies/ads</a>.</p>

    <h3 style="margin-top:1.5rem;">Affiliate Links & Third Party Networks</h3>
    <p>TechSpec contains affiliate marketing links (primarily to Amazon.in). When you click on an affiliate link, a third-party cookie may be set by the affiliate network to track qualifying purchases. Please review the respective privacy policies of these third-party platforms for detailed information regarding their practices.</p>

    <h3 style="margin-top:1.5rem;">Consent</h3>
    <p>By using our website, you hereby consent to our Privacy Policy and agree to its Terms and Conditions.</p>
"""),
        ("disclaimer.html", "Affiliate Disclaimer & Disclosure - TechSpec India", "Full Amazon Associates and affiliate disclosure for TechSpec India. FTC and Amazon compliance statements.", "disclaimer", """
    <h1>Affiliate Disclosure & Disclaimer</h1>
    <p style="color:var(--text-muted); margin-bottom:2rem;">Last Updated: November 2026</p>

    <div class="winner-banner" style="margin-bottom:2rem;">
      <h3>Amazon Associates Program Disclosure</h3>
      <p style="font-size:1.05rem; line-height:1.6; color:#f8fafc;">
        <strong>TechSpec India</strong> is a participant in the Amazon Services LLC Associates Program and the Amazon.in Associates Programme, affiliate advertising programs designed to provide a means for websites to earn advertising fees by advertising and linking to Amazon.in (and related international Amazon domains).
      </p>
    </div>

    <h3>What Does This Mean For You?</h3>
    <p>When you click on a "Check Latest Price on Amazon.in" button or any affiliate link on TechSpec and subsequently purchase a laptop or accessory, Amazon pays us a small referral commission.</p>
    <p><strong class="text-emerald">This comes at absolutely NO extra cost to you.</strong> The price you pay on Amazon is identical whether you visit through our site, search directly, or use any other link.</p>

    <h3 style="margin-top:2rem;">Editorial Integrity & No Biased Placements</h3>
    <p>Our editorial ratings, benchmark analyses, and comparisons are strictly objective and data-driven. We highlight severe flaws—such as 45W low TGP bottlenecks, 45% NTSC color reproduction, and soldered RAM—regardless of manufacturer relationships or commissions.</p>
    <p>We do not accept payment to promote or rank any particular laptop higher on our buying guides.</p>

    <h3 style="margin-top:2rem;">Pricing and Availability Disclaimer</h3>
    <p>Laptop prices, bank discounts (e.g. HDFC / ICICI card offers), and stock availability in India fluctuate rapidly. While our database strives to reflect prevailing market rates, please confirm the final landed cost on the retailer's checkout page before completing your transaction.</p>
""")
    ]

    for fname, title, desc, nav_key, body in pages:
        canonical_path = f"/{fname}"
        html_content = get_common_head(title, desc, canonical_path, "website")
        html_content += get_header(active_nav=nav_key)
        html_content += f"""  <main class="content-container" style="padding-top:2rem; max-width:850px;">
    <div class="breadcrumbs">
      <a href="/">Home</a> &gt; <span>{title.split(' - ')[0]}</span>
    </div>
    <div class="detail-header" style="line-height:1.8;">
{body}
    </div>
  </main>
"""
        html_content += get_footer()
        (DIST_DIR / fname).write_text(html_content, encoding="utf-8")

def generate_comparisons_dataset(laptops):
    """
    Generate 80+ high-value, realistic head-to-head comparison pairings.
    Pairs laptops within reasonable price brackets or same GPU tiers.
    """
    comparisons = []
    seen = set()

    n = len(laptops)
    for i in range(n):
        for j in range(i + 1, n):
            lap_a = laptops[i]
            lap_b = laptops[j]

            # Criterion for high-search matchup:
            # 1. Same GPU tier (e.g. RTX 3050 vs RTX 3050, RTX 4050 vs RTX 4050, RTX 4060 vs RTX 4060)
            # 2. Price difference <= 25,000 INR
            # 3. Direct rival lines (e.g. TUF vs LOQ, Victus vs Nitro, Strix vs Helios Neo)
            same_gpu = lap_a["gpu_tier"] == lap_b["gpu_tier"]
            price_close = abs(lap_a["price_inr"] - lap_b["price_inr"]) <= 28000
            rival_brand = lap_a["brand"] != lap_b["brand"]
            is_upgrade_pair = lap_a["brand"] == lap_b["brand"] and abs(lap_a["price_inr"] - lap_b["price_inr"]) <= 35000

            if not (same_gpu or price_close or is_upgrade_pair):
                continue

            slug = f"{lap_a['slug']}-vs-{lap_b['slug']}"
            if slug in seen:
                continue
            seen.add(slug)

            # Determine winner logic
            # Weighted score: gaming (0.35), coding (0.2), value (0.3), battery (0.15)
            def calc_score(l):
                s = l["scores"]
                return s["gaming"] * 0.35 + s["coding"] * 0.20 + s["value_for_money"] * 0.30 + s["battery_portability"] * 0.15

            score_a = calc_score(lap_a)
            score_b = calc_score(lap_b)

            if score_a >= score_b:
                winner = "a"
                win_l = lap_a
                lose_l = lap_b
            else:
                winner = "b"
                win_l = lap_b
                lose_l = lap_a

            # Formulate verdict explanation
            advantages = []
            if win_l["tgp_watts"] > lose_l["tgp_watts"]:
                advantages.append(f"higher {win_l['tgp_watts']}W GPU TGP (vs {lose_l['tgp_watts']}W)")
            if "100% sRGB" in win_l["color_gamut"] and "100% sRGB" not in lose_l["color_gamut"]:
                advantages.append("richer 100% sRGB color-accurate display")
            if win_l["price_inr"] < lose_l["price_inr"]:
                advantages.append(f"saving you {format_inr(lose_l['price_inr'] - win_l['price_inr'])}")
            if win_l["scores"]["gaming"] > lose_l["scores"]["gaming"]:
                advantages.append("superior frame rates in AAA benchmarks")
            if win_l["scores"]["battery_portability"] > lose_l["scores"]["battery_portability"]:
                advantages.append("better battery endurance")

            if not advantages:
                advantages.append("superior overall value for money and thermal balance")

            adv_str = ", ".join(advantages)
            verdict_full = f"We recommend the <strong>{win_l['name']}</strong> as the overall winner in this matchup due to its {adv_str}. However, consider the {lose_l['name']} if you prefer its specific brand ecosystem or aesthetic design."
            verdict_short = f"{win_l['name']} takes the win with {adv_str}."

            comparisons.append({
                "slug": slug,
                "lap_a": lap_a,
                "lap_b": lap_b,
                "winner": winner,
                "verdict_full": verdict_full,
                "verdict_short": verdict_short
            })

    return comparisons

def generate_sitemap_and_robots(all_urls):
    today = datetime.date.today().isoformat()
    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    for url in all_urls:
        priority = "1.0" if url == "/" else ("0.9" if "/laptops/" in url or "/compare/" in url else "0.8")
        sitemap_xml.append(f"  <url>")
        sitemap_xml.append(f"    <loc>{SITE_URL}{url}</loc>")
        sitemap_xml.append(f"    <lastmod>{today}</lastmod>")
        sitemap_xml.append(f"    <changefreq>weekly</changefreq>")
        sitemap_xml.append(f"    <priority>{priority}</priority>")
        sitemap_xml.append(f"  </url>")

    sitemap_xml.append('</urlset>')
    (DIST_DIR / "sitemap.xml").write_text("\n".join(sitemap_xml), encoding="utf-8")

    robots_txt = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (DIST_DIR / "robots.txt").write_text(robots_txt, encoding="utf-8")

def main():
    print("=" * 60)
    print("TechSpec India - Static Site Generator")
    print(f"Target Output: {DIST_DIR}")
    print("=" * 60)

    # 1. Prepare directories
    (DIST_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "laptops").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "compare").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "guides").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "accessories").mkdir(parents=True, exist_ok=True)

    # 2. Load dataset
    laptops, accessories, guides = load_data()
    print(f"Loaded {len(laptops)} laptops, {len(accessories)} accessories, {len(guides)} buying guides.")

    laptops_by_slug = {lap["slug"]: lap for lap in laptops}

    # 3. Generate assets & scripts
    generate_css()
    generate_config_js()
    generate_app_js()
    print("Generated style.css, config.js, and app.js")

    all_urls = ["/"]

    # 4. Generate Comparisons
    comparisons = generate_comparisons_dataset(laptops)
    print(f"Generated {len(comparisons)} head-to-head comparison matchups.")

    # 5. Generate Homepage
    generate_homepage(laptops, comparisons, guides, accessories)
    print("Generated index.html (Homepage)")

    # 6. Generate Laptop Review & Spec Pages
    for lap in laptops:
        # Filter comparisons relevant to this laptop
        lap_comps = [c for c in comparisons if c["lap_a"]["slug"] == lap["slug"] or c["lap_b"]["slug"] == lap["slug"]]
        generate_laptop_page(lap, lap_comps)
        all_urls.append(f"/laptops/{lap['slug']}.html")
    print(f"Generated {len(laptops)} individual laptop spec & review pages.")

    # 7. Generate Comparison Pages
    for cmp in comparisons:
        generate_comparison_page(cmp)
        all_urls.append(f"/compare/{cmp['slug']}.html")
    print(f"Generated {len(comparisons)} head-to-head comparison pages.")

    # 8. Generate Guide Pages
    for g in guides:
        generate_guide_page(g, laptops_by_slug)
        all_urls.append(f"/guides/{g['slug']}.html")
    print(f"Generated {len(guides)} buyer guide pages.")

    # 9. Generate Accessories Hub and Product Pages
    generate_accessories_hub(accessories)
    all_urls.append("/accessories/index.html")
    for acc in accessories:
        generate_accessory_page(acc)
        all_urls.append(f"/accessories/{acc['slug']}.html")
    print(f"Generated {len(accessories) + 1} accessories pages.")

    # 10. Generate Legal / AdSense Pages
    generate_legal_pages()
    for fname in ["about.html", "contact.html", "privacy-policy.html", "disclaimer.html"]:
        all_urls.append(f"/{fname}")
    print("Generated legal trust & AdSense compliance pages.")

    # 11. Generate Sitemap & Robots.txt
    generate_sitemap_and_robots(all_urls)
    print(f"Generated sitemap.xml with {len(all_urls)} URLs and robots.txt.")

    print("=" * 60)
    print(f"BUILD COMPLETE: Successfully generated {len(all_urls)} total HTML pages in dist/")
    print("=" * 60)

if __name__ == "__main__":
    main()
