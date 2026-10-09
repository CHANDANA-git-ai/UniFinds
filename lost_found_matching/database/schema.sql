CREATE TABLE IF NOT EXISTS reports (
 id INTEGER PRIMARY KEY AUTOINCREMENT, report_type TEXT NOT NULL CHECK(report_type IN ('LOST','FOUND')),
 item_name TEXT NOT NULL, description TEXT, category TEXT, color TEXT, location_name TEXT,
 latitude REAL, longitude REAL, event_date TEXT, event_time TEXT, image_path TEXT,
 status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE','MATCHED','CLOSED')),
 user_id INTEGER,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS matches (
 id INTEGER PRIMARY KEY AUTOINCREMENT, lost_report_id INTEGER NOT NULL, found_report_id INTEGER NOT NULL,
 image_score REAL, text_score REAL, attribute_score REAL, location_score REAL, time_score REAL,
 final_score REAL NOT NULL, confidence TEXT NOT NULL, explanation TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(lost_report_id) REFERENCES reports(id), FOREIGN KEY(found_report_id) REFERENCES reports(id),
 UNIQUE(lost_report_id, found_report_id)
);
CREATE INDEX IF NOT EXISTS idx_reports_type_status ON reports(report_type, status);

-- Users table for student accounts
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 full_name TEXT NOT NULL,
 usn TEXT UNIQUE,
 email TEXT NOT NULL UNIQUE,
 password_hash TEXT NOT NULL,
 department TEXT,
 year TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
