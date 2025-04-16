# MongoDB - Final Project

This project is a sample application for tracking player statistics for a hypothetical online service game. It demonstrates how to use MongoDB as a backend (with a defined schema and sample commands), a Flask-based REST API (with and without Swagger documentation), and a Tkinter-based GUI for basic CRUD operations.

## Overview

- **Database:** MongoDB  
- **API:** Flask/Flask‑RESTx (Swagger available)  
- **Frontend:** Tkinter GUI  
- **Included Utilities:**  
  - *Collection Builder.js* – Script to build the collection and insert sample data.  
  - *Base Queries.js* – Script with base queries for testing the MongoDB collection.

## Features

- **MongoDB Schema:**  
  Each player document includes:
  - `player_id`, `username`
  - `stats`: Contains detailed player statistics, including:
    - **Overall**: rounds played, wins, score, time played (in days)
    - **Combat Breakdown**:  
      - *Kills*: categorized by headshot, lock-on, other, and an overall total  
      - *Deaths*: categorized by headshot, lock-on, other, and an overall total  
      - *Stuns*: categorized by headshot, lock-on, other, and an overall total  
      - *Stuns Received*: categorized by headshot, lock-on, other, and an overall total  
    - **Additional Stats**:  
      consecutive kills, consecutive deaths, consecutive headshots, suicides, friendly kills, friendly stuns, times stunned, CQC attacks given, CQC attacks taken, rolls, salutes, catapult uses, bases captured, radio uses, chat uses, knife kills, and knife stuns.
  - `login_info`: last_login, login_count, ip_address
  - `hardware_info`: cpu, gpu, os, ram
  - `profile`, `created_at`, and `animal_rank`

- **API & GUI:**  
  - **API:** Create, read, update, and delete player records.  
  - **Swagger UI:** Interactive API documentation (if using the Swagger version).  
  - **GUI:** A desktop interface to view, edit, and add players.

## File Structure


- `app_swagger.py` – Flask API with Swagger documentation.  
- `frontend.py` – Tkinter GUI for managing player data.
- `app.py` – Flask API (non‑Swagger version for if localhost gives issues).
- `Collection Builder.js` – Script to build the MongoDB collection and add sample data.  
- `Base Queries.js` – File with basic MongoDB queries to test the collection with.

## Setup and Running

### Prerequisites

- **MongoDB:** Install and run MongoDB in replica set mode.  
- **Python:** Version 3.12+
- **Dependencies:** Install with:
  `pip install flask flask-restx pymongo`
