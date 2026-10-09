"""SQLite persistence for the lost-and-found matching service."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any
from passlib.hash import pbkdf2_sha256 as _hasher

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = ROOT / "database" / "lost_found.db"

class Database:
    def __init__(self, path: str | Path = DEFAULT_DB_PATH):
        self.path = str(path)
        self.initialize()
    def connect(self):
        con = sqlite3.connect(self.path); con.row_factory = sqlite3.Row; return con
    def initialize(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        schema = (Path(__file__).with_name("schema.sql")).read_text(encoding="utf-8")
        with self.connect() as con: con.executescript(schema)
        # Migrate existing DB: ensure 'user_id' column exists on reports
        with self.connect() as con:
            cur = con.execute("PRAGMA table_info('reports')")
            cols = [r[1] for r in cur.fetchall()]
            if 'user_id' not in cols:
                try:
                    con.execute("ALTER TABLE reports ADD COLUMN user_id INTEGER")
                except Exception:
                    pass
    def create_report(self, **data: Any) -> int:
        required = {"report_type", "item_name"}
        if not required <= data.keys(): raise ValueError("report_type and item_name are required")
        data["report_type"] = str(data["report_type"]).upper()
        if data["report_type"] not in {"LOST", "FOUND"}: raise ValueError("report_type must be LOST or FOUND")
        columns = [k for k in data if k in REPORT_COLUMNS]
        values = [data[k] for k in columns]
        with self.connect() as con:
            cur=con.execute(f"INSERT INTO reports ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})", values)
            return cur.lastrowid
    def get_report(self, report_id: int):
        with self.connect() as con:
            row=con.execute("SELECT * FROM reports WHERE id=?", (report_id,)).fetchone()
        return dict(row) if row else None

    # User helpers
    def create_user(self, full_name: str, email: str, password: str, usn: str = None, department: str = None, year: str = None):
        pwd_hash = _hasher.hash(password)
        with self.connect() as con:
            cur = con.execute("INSERT INTO users (full_name, usn, email, password_hash, department, year) VALUES (?,?,?,?,?,?)", (full_name, usn, email, pwd_hash, department, year))
            return cur.lastrowid

    def get_user_by_email_or_usn(self, identifier: str):
        with self.connect() as con:
            row = con.execute("SELECT * FROM users WHERE email=? COLLATE NOCASE", (identifier,)).fetchone()
            if row: return dict(row)
            row = con.execute("SELECT * FROM users WHERE usn=?", (identifier,)).fetchone()
            return dict(row) if row else None

    def verify_user_password(self, identifier: str, password: str) -> dict | None:
        user = self.get_user_by_email_or_usn(identifier)
        if not user: return None
        if _hasher.verify(password, user['password_hash']):
            return user
        return None
    def get_all_reports(self):
        with self.connect() as con: rows=con.execute("SELECT * FROM reports ORDER BY id").fetchall()
        return [dict(x) for x in rows]
    def get_active_reports(self): return self._query("SELECT * FROM reports WHERE status='ACTIVE' ORDER BY id")
    def get_opposite_reports(self, report_type: str):
        kind="FOUND" if report_type.upper()=="LOST" else "LOST"
        return self._query("SELECT * FROM reports WHERE report_type=? AND status='ACTIVE' ORDER BY id", (kind,))
    def update_report_status(self, report_id: int, status: str):
        status=status.upper()
        if status not in {"ACTIVE","MATCHED","CLOSED"}: raise ValueError("invalid status")
        with self.connect() as con:
            cur=con.execute("UPDATE reports SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (status,report_id))
            return cur.rowcount > 0
    def delete_report(self, report_id: int):
        with self.connect() as con:
            con.execute("DELETE FROM matches WHERE lost_report_id=? OR found_report_id=?",(report_id,report_id))
            return con.execute("DELETE FROM reports WHERE id=?",(report_id,)).rowcount > 0
    def upsert_match(self, **m):
        columns=list(m); vals=[m[k] for k in columns]
        updates=','.join(f"{c}=excluded.{c}" for c in columns if c not in {'lost_report_id','found_report_id'})
        with self.connect() as con: con.execute(f"INSERT INTO matches ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)}) ON CONFLICT(lost_report_id,found_report_id) DO UPDATE SET {updates}",vals)
    def _query(self, sql, params=()):
        with self.connect() as con: rows=con.execute(sql,params).fetchall()
        return [dict(x) for x in rows]
REPORT_COLUMNS={'report_type','item_name','description','category','color','location_name','latitude','longitude','event_date','event_time','image_path','status'}
