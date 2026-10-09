from lost_found_matching.database.db import Database
class ReportService:
    def __init__(self, db=None): self.db=db or Database()
    def create_report(self, **kwargs): return self.db.create_report(**kwargs)
    def get_report(self, report_id): return self.db.get_report(report_id)
    def get_all_reports(self): return self.db.get_all_reports()
    def get_active_reports(self): return self.db.get_active_reports()
    def get_opposite_reports(self, report_type): return self.db.get_opposite_reports(report_type)
    def update_report_status(self, report_id, status): return self.db.update_report_status(report_id,status)
    def delete_report(self, report_id): return self.db.delete_report(report_id)
_service=ReportService()
create_report=_service.create_report; get_report=_service.get_report; get_all_reports=_service.get_all_reports; get_active_reports=_service.get_active_reports; get_opposite_reports=_service.get_opposite_reports; update_report_status=_service.update_report_status; delete_report=_service.delete_report
