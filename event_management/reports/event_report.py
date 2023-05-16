from odoo import models, api


class EventReport(models.AbstractModel):
    _name = "report.event_management.report_event"
    """abstract model for report"""

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model':'report.wizard',
            # 'docs': docs,
            'data': data,

        }

